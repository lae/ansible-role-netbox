from extras.reports import Report


class NothingReport(Report):
    description = "A report."

    def test_nothing(self):
        self.log_success("Success! Hm? What is, you ask? That's a secret.")
