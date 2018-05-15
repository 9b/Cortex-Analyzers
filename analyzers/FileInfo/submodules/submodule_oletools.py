"""FileInfo oletools submodule; WIP"""
from .submodule_base import SubmoduleBaseclass
from oletools.oleid import OleID
from oletools.olevba3 import  VBA_Parser_CLI
from oletools.msodde import process_file


class OLEToolsSubmodule(SubmoduleBaseclass):
    """Try to inspect files using python oletools."""

    def __init__(self):
        SubmoduleBaseclass.__init__(self)
        self.name = 'Oletools Submodule'

    def check_file(self, **kwargs):
        """Oletools accepts MS office documents."""

        try:
            if kwargs.get('filetype') in [
                'DOC',
                'DOCM',
                'DOCX',
                'XLS',
                'XLSM',
                'XLSX',
                'PPT',
                'PPTM',
                'PPTX'
            ]:
                return True
        except KeyError:
            return False
        return False

    def analyze_file(self, path):
        # Run the analyze functions
        #self.analyze_oleid(path)
        self.analyze_vba(path)
        self.analyze_dde(path)

        return self.results

    # def analyze_oleid(self, path):
    #     indicators = OleID(path).check()
    #     results = {}
    #
    #     for indicator in indicators:
    #         if indicator.id == 'appname':
    #             continue
    #         results.update({indicator.name: indicator.value})
    #     self.add_result_subsection('Oletools OleID Results', results)

    def analyze_vba(self, path):
        """Analyze a given sample for malicios vba."""
        try:

            vba_parser = VBA_Parser_CLI(path, relaxed=True)
            vbaparser_result = vba_parser.process_file_json(show_decoded_strings=True,
                                                            display_code=True,
                                                            hide_attributes=False,
                                                            vba_code_only=False,
                                                            show_deobfuscated_code=True,
                                                            deobfuscate=True)
            self.add_result_subsection('Olevba', vbaparser_result)
        except TypeError:
            self.add_result_subsection('Oletools VBA Analysis failed', 'Analysis failed due to an filetype error.'
                                                                 'The file does not seem to be a valid MS-Office file.')

    def analyze_dde(self, path):
        results = process_file(path)
        if len(results) > 0:
            self.add_result_subsection('Oletools DDE Analysis', {'DDEUrl': results})
        else:
            self.add_result_subsection('Oletools DDE Analysis', {'Info': 'No DDE URLs found.'})
