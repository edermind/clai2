import pytest
from pathlib import Path
from core.file_handler import inject_files


def test_no_files_in_prompt():
    """Промпт без @ возвращается без изменений."""
    prompt = "сколько фигур в шахматах"
    assert inject_files(prompt) == prompt


def test_single_file_injected(tmp_path):
    """@ заменяется на содержимое файла."""
    f = tmp_path / "test.txt"
    f.write_text("hello world")

    result = inject_files(f"прочитай @{f}")

    assert "hello world" in result
    assert str(f) in result


def test_multiple_files_injected(tmp_path):
    """Несколько @ заменяются все."""
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("содержимое A")
    f2.write_text("содержимое B")

    result = inject_files(f"сравни @{f1} и @{f2}")

    assert "содержимое A" in result
    assert "содержимое B" in result


def test_missing_file_exits(tmp_path):
    """Несуществующий файл — SystemExit."""
    with pytest.raises(SystemExit):
        inject_files("читай @/несуществующий/файл.txt")