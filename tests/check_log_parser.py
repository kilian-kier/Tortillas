import logging
from tortillas.log_parser import LogParser
from tortillas.tortillas_config import AnalyzeConfigEntry


def test_log_splitting():
    config_entry = AnalyzeConfigEntry(name='test',
                                      scope='SYSCALL',
                                      pattern=r'(.*)',
                                      mode='').compile_pattern()

    log_parser = LogParser(log_file_path='./tests/assets/out_log.txt',
                           config=[config_entry])

    log_data = log_parser.parse()

    assert config_entry.name in log_data
    assert ('Syscall::EXIT: called, exit_code: 1237619379\n'
            in log_data[config_entry.name])


def test_parsing_int_splitting():
    config_entry = AnalyzeConfigEntry(name='test',
                                      scope='SYSCALL',
                                      pattern=r'exit_code: (\d+)',
                                      mode='')

    config_entry.compile_pattern()

    log_parser = LogParser(log_file_path='./tests/assets/out_log.txt',
                           config=[config_entry])

    log_data = log_parser.parse()

    assert config_entry.name in log_data
    assert '1237619379' in log_data[config_entry.name]


def test_multiple_config_entries():
    config = [
            AnalyzeConfigEntry(name='a', scope='SYSCALL',
                               pattern='(.*)', mode=''),
            AnalyzeConfigEntry(name='b', scope='THREAD',
                               pattern='(kill: (.*))', mode=''),
            AnalyzeConfigEntry(name='c', scope='PAGEFAULT',
                               pattern=r'(Address:\s+0x[0-9a-fA-F]+)',
                               mode='')]

    for entry in config:
        entry.compile_pattern()

    log_parser = LogParser(log_file_path='./tests/assets/out_log.txt',
                           config=config)

    log_data = log_parser.parse()

    for entry in config:
        assert entry.name in log_data.keys()

    assert any('kill' in log for log in log_data['b'])
    assert 'Address:          0x8006000' in log_data['c']
