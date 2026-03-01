import pytest
from pathlib import Path

from decorators import timer, validate_file, log_call


def test_timer_returns_correct_value():
    @timer
    def summ(a, b):
        return a + b

    assert summ(1, 2) == 3


def test_timer_prints_message(capsys):
    @timer
    def summ(a, b):
        return a + b

    summ(1,2)
    captured = capsys.readouterr()

    assert "выполнилась за" in captured.out

def test_timer_preserves_name():
    @timer
    def my_func():
        pass
    
    assert my_func.__name__ == "my_func"


def test_validate_existed_file(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("content")

    @validate_file
    def read_file(file):
        with open(file, 'r', encoding='utf-8') as f:
            data = f.readline()
        return data

    assert read_file(file) == "content"

def test_validate_unexisted_file():

    @validate_file
    def read_file(file):
        with open(file, 'r', encoding='utf-8') as f:
            data = f.readline()
        return data

    with pytest.raises(FileNotFoundError, match="Файл test.csv не найден"):
        read_file("test.csv")

def test_validate_not_csv_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content")

    @validate_file
    def read_file(file):
        with open(file, 'r', encoding='utf-8') as f:
            data = f.readline()
        return data

    with pytest.raises(ValueError, match="Ожидается .csv файл, получен: .txt"):
        read_file(file)


def test_add_valid_message_to_log_file(tmp_path):
    file = tmp_path / "tracker.log"
    
    @log_call(file)
    def my_func():
        pass
    
    my_func()
    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    assert len(data) == 1
    assert "my_func" in data[0]

def test_add_some_messages_to_log_file(tmp_path):
    file = tmp_path / "tracker.log"
    
    @log_call(file)
    def my_func():
        pass
    
    my_func()
    my_func()
    my_func()

    with open(file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    assert len(data) == 3

    