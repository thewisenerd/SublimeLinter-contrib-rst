from SublimeLinter.lint import Linter, LintMatch  # or NodeLinter, PythonLinter, ComposerLinter, RubyLinter
import logging
import json

logger = logging.getLogger('SublimeLinter.plugin.rstlint')

class RstLint(Linter):
    multiline = False
    defaults = {
        'selector': 'text.restructuredtext'
    }

    def cmd(self):
        print(self.filename)
        return ['rst-lint', '--format=json', self.filename]

    def find_errors(self, output):
        """Parse errors from linter's output."""
        try:
            content = json.loads(output)
        except ValueError:
            logger.error(
                "JSON Decode error: We expected JSON from 'rst-lint', "
                "but instead got this:\n{}\n\n".format(output))
            self.notify_failure()
            return

        for entry in content:
            print(entry)
            filename = entry.get('source', None)

            yield LintMatch(
                match=None,
                line=entry['line'] - 1, # zero indexed
                col=None,
                error=None,
                warning=None,
                message=entry['message'],
                near=None,
                filename=filename,
                error_type='error' if entry['level'] >= 3 else 'warning',
                code=None
            )
