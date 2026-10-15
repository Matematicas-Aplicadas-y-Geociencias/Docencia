from datetime import datetime
from pathlib import Path

import httpx
import pytest

from pull_dataset_hycom_tsis_gomb0p01_1s100 import (
    DownloadSettings,
    DownloadStatus,
    create_download_url,
    create_file_info,
    download_data,
    parse_and_validate_date_range,
    stream_to_file,
    request_data,
)


#
# Test create_download_url
#
def test_create_download_url_returns_correct_url():
    url = create_download_url("010_archv.2001_365_18_2d.nc", 2001)
    assert (
        str(url)
        == "https://tds.hycom.org/thredds/fileServer/datasets/GOMb0.01/reanalysis/data/2001/010_archv.2001_365_18_2d.nc"
    )


def test_create_download_url_uses_correct_year_in_path():
    url_2001 = create_download_url("archivo.nc", 2001)
    url_2024 = create_download_url("archivo.nc", 2024)
    assert "/2001/" in str(url_2001)
    assert "/2024/" in str(url_2024)


#
# Test create_file_info
#
def test_create_file_info_returns_correct_filename():
    date = datetime(2001, 12, 31, 18)  # anio=2001, dia=365, hora=18
    result = create_file_info(date)
    assert result.name == "010_archv.2001_365_18_2d.nc"


def test_create_file_info_returns_correct_directory():
    date = datetime(2001, 12, 31, 18)
    result = create_file_info(date)
    assert result.parent == Path("datos_hycomm_1_100/2001")


def test_create_file_info_zeros_pads_hour():
    date = datetime(2002, 1, 18, 0)  # hora=0, debe ser "00"
    result = create_file_info(date)
    assert "_00_" in result.name


def test_create_file_info_returns_path_object():
    date = datetime(2001, 12, 31, 18)
    result = create_file_info(date)
    assert isinstance(result, Path)


#
# Test parse_and_validate_date_range
#
def test_parse_and_validate_date_range_returns_correct_dates():
    start_date, end_date = parse_and_validate_date_range(
        "2001-365-18", "2002-001-00", "%Y-%j-%H"
    )
    assert start_date == datetime(2001, 12, 31, 18)
    assert end_date == datetime(2002, 1, 1, 0)


def test_parse_and_validate_date_range_same_date_is_valid():
    start_date, end_date = parse_and_validate_date_range(
        "2012-016-01", "2012-016-01", "%Y-%j-%H"
    )
    assert start_date == end_date


def test_parse_and_validate_date_range_invalid_format_raises_value_error():
    with pytest.raises(ValueError):
        parse_and_validate_date_range("2003/11/22", "2004-011-01", "%Y-%j-%H")


def test_parse_and_validate_date_range_invalid_hour_raises_value_error():
    with pytest.raises(ValueError):
        parse_and_validate_date_range("2003-011-25", "2004-011-01", "%Y-%j-%H")


def test_parse_and_validate_date_range_invalid_day_raises_value_error():
    with pytest.raises(ValueError):
        parse_and_validate_date_range("2003-011-22", "2004-367-01", "%Y-%j-%H")


def test_parse_and_validate_date_range_start_after_end_raises_value_error():
    with pytest.raises(ValueError):
        parse_and_validate_date_range("2012-045-01", "2011-045-00", "%Y-%j-%H")


#
# Test download_data
#
def test_download_data_success(mocker, tmp_path):
    # Se intercepta httpx.Client
    mock_client = mocker.patch("pull_dataset_hycom_tsis_gomb0p01_1s100.httpx.Client")

    # 2. Se simula la response
    mock_response = mocker.MagicMock()
    mock_response.headers = {"content-length": "100"}
    mock_response.iter_bytes.return_value = [b"chunk1", b"chunk2"]
    mock_response.raise_for_status.return_value = None

    # Se concecta la cadena: client.stream().__enter__() -> response
    mock_client.return_value.__enter__.return_value.stream.return_value.__enter__.return_value = mock_response

    # 4. Se ejecuta
    url = httpx.URL("https://example.com/file.nc")
    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=0)

    result = download_data(url, output_file, settings)

    assert result == DownloadStatus.SUCCESS


def test_download_data_request_error_retries_and_returns_failed(mocker, tmp_path):
    mock_client = mocker.patch("pull_dataset_hycom_tsis_gomb0p01_1s100.httpx.Client")

    # Se simula que stream lanza RequestError
    mock_client.return_value.__enter__.return_value.stream.side_effect = (
        httpx.RequestError("connection failed")
    )

    url = httpx.URL("https://example.com/file.nc")
    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=1)

    result = download_data(url, output_file, settings)

    assert result == DownloadStatus.FAILED


def test_download_data_request_http_error_temporal_retries_and_returns_failed(
    mocker, tmp_path
):
    mock_client = mocker.patch("pull_dataset_hycom_tsis_gomb0p01_1s100.httpx.Client")

    # Se simula una response con status 503
    mock_response = mocker.MagicMock()
    mock_response.status_code = 503
    mock_client.return_value.__enter__.return_value.stream.return_value.__enter__.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "503", request=mocker.MagicMock(), response=mock_response
    )

    url = httpx.URL("https://example.com/file.nc")
    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=1)

    result = download_data(url, output_file, settings)

    assert result == DownloadStatus.FAILED


def test_download_data_succeds_on_third_retry(mocker, tmp_path):
    mock_client = mocker.patch("pull_dataset_hycom_tsis_gomb0p01_1s100.httpx.Client")

    mock_response = mocker.MagicMock()
    mock_response.headers = {"content-length": "100"}
    mock_response.iter_bytes.return_value = [b"chunck1", b"chunck2", b"chunck3"]
    mock_response.raise_for_status.return_value = None

    # Las dos primeras llamadas fallan, la tercera devuelve el response exitoso
    mock_client.return_value.__enter__.return_value.stream.side_effect = [
        httpx.RequestError("Error 1"),
        httpx.RequestError("Error 2"),
        mock_client.return_value.__enter__.return_value.stream.return_value,  # reintento exitoso
    ]

    mock_client.return_value.__enter__.return_value.stream.return_value.__enter__.return_value = mock_response

    url = httpx.URL("https://example.com/file.nc")
    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=1)

    result = download_data(url, output_file, settings)

    assert result == DownloadStatus.SUCCESS
    # Verificamos que intentó 2 veces an
    assert mock_client.call_count == 3  # Intento inicial + 2 reintentos


def test_download_data_http_404_returns_failed_immediately(mocker, tmp_path):
    mock_client = mocker.patch("pull_dataset_hycom_tsis_gomb0p01_1s100.httpx.Client")

    # Se simula un error permanente (status code 404)
    mock_response = mocker.MagicMock()
    mock_response.status_code = 404
    mock_client.return_value.__enter__.return_value.stream.return_value.__enter__.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404", request=mocker.MagicMock(), response=mock_response
    )

    url = httpx.URL("https://example.com/file.nc")
    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=1)

    result = download_data(url, output_file, settings)

    assert result == DownloadStatus.FAILED
    # Verificamos que solo intentó una vez, no más de una
    assert mock_client.call_count == 1


def test_download_data_unexpected_exception_retries_and_returns_failed(
    mocker, tmp_path
):
    mock_client = mocker.patch("pull_dataset_hycom_tsis_gomb0p01_1s100.httpx.Client")

    mock_client.return_value.__enter__.return_value.stream.side_effect = Exception(
        "Unexpected error"
    )
    url = httpx.URL("https://example.com/file.nc")
    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=1)

    result = download_data(url, output_file, settings)

    assert result == DownloadStatus.FAILED
    # Verificamos que intentó 3 veces antes de fallar
    assert mock_client.call_count == 4  # Intento inicial + 3 reintentos


#
# Test stream_to_file
#
def test_stream_to_file_writes_chunks_to_disk(mocker, tmp_path):
    mock_response = mocker.MagicMock()
    mock_response.iter_bytes.return_value = [b"chunkA", b"chunkB", b"chunkC"]

    output_file = tmp_path / "file.nc"
    downloaded = stream_to_file(
        mock_response, output_file, total_size=0, chunk_size=1024
    )

    assert output_file.read_bytes() == b"chunkAchunkBchunkC"


def test_stream_to_file_return_correct_byte_count(mocker, tmp_path):
    mock_response = mocker.MagicMock()
    mock_response.iter_bytes.return_value = [b"chunkA", b"chunkB", b"chunkC"]

    output_file = tmp_path / "file.nc"
    downloaded = stream_to_file(
        mock_response, output_file, total_size=0, chunk_size=1024
    )

    assert downloaded == len(b"chunkAchunkBchunkC")


def test_stream_to_file_ignores_empty_chunks(mocker, tmp_path):
    mock_response = mocker.MagicMock()
    mock_response.iter_bytes.return_value = [b"chunkA", b"", b"chunkC"]

    output_file = tmp_path / "file.nc"
    downloaded = stream_to_file(
        mock_response, output_file, total_size=0, chunk_size=1024
    )

    assert downloaded == len(b"chunkAchunkC")


#
# Test request_data
#
def test_request_data_propagates_http_status_error(tmp_path, mocker):
    mock_client= mocker.MagicMock()
    mock_response = mocker.MagicMock()
    mock_response.status_code = 503
    mock_client.stream.return_value.__enter__.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
        "503", request=mocker.MagicMock(), response=mock_response
    )

    output_file = tmp_path / "file.nc"
    settings = DownloadSettings(retries_number=3, sleep_time=1)

    with pytest.raises(httpx.HTTPStatusError):
        request_data(mock_client, httpx.URL("https://example.com/file.nc"), output_file ,settings)