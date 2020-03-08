from extras.scripts import Script


class Nothing(Script):
    def run(self, data, commit=False):
        return ""
