from cuda_lint import Linter
from . import yaml

class PyYaml(Linter):
    """Provides an interface to pyyaml."""

    syntax = 'YAML'
    cmd = None
    regex = r'^:(?P<line>\d+):(?P<col>\d+): (?P<message>.+)'
    line_col_base = (0, 0)  # the lines and columns are 0-based

    def run(self, cmd, code):
        try:
            for x in yaml.safe_load_all(code):
                # exhausting generator so all documents are checked
                pass
        except yaml.error.YAMLError as exc:
            message = '{}: {}: {}'.format(
                type(exc).__name__, exc.problem, exc.context)
            return ':{}:{}: {}\n'.format(
                exc.problem_mark.line, exc.problem_mark.column, message)
        except Exception as exc:
            msg = '{} - uncaught exception - {} : {}'.format(
                self.name, type(exc), exc)
            print('Linter for yaml:', msg)
        return ''
