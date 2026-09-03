from django.db import models


class VidhanSabhaElectionWinners(models.Model):
    """Vidhan Sabha winners data (sheet: first)."""

    assembly_no = models.IntegerField(db_index=True)
    constituency_no = models.IntegerField(db_index=True)
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(null=True, blank=True)
    delim_id = models.IntegerField(null=True, blank=True)
    poll_no = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    candidate = models.CharField(max_length=255, db_index=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    party = models.CharField(max_length=100, db_index=True)
    votes = models.FloatField(null=True, blank=True)
    age_of_winner = models.FloatField(null=True, blank=True)
    average_age_of_contestants = models.FloatField(null=True, blank=True)
    candidate_type = models.CharField(max_length=50, null=True, blank=True)
    no_of_valid_votes_casted = models.FloatField(null=True, blank=True)
    no_of_registered_electors = models.FloatField(null=True, blank=True)
    select_constituency = models.CharField(max_length=200, db_index=True)
    constituency_type = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    district = models.CharField(max_length=100, db_index=True)
    sub_region = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    no_of_candidates = models.FloatField(null=True, blank=True)
    turnout_rate = models.FloatField(null=True, blank=True)
    vote_share = models.FloatField(null=True, blank=True)
    deposit_lost = models.CharField(max_length=20, null=True, blank=True)
    winning_margin = models.FloatField(null=True, blank=True)
    winning_margin_percentage = models.FloatField(null=True, blank=True)
    enop = models.FloatField(null=True, blank=True)
    pid = models.CharField(max_length=50, null=True, blank=True)
    party_type_tcpd = models.CharField(max_length=100, null=True, blank=True)
    party_id = models.IntegerField(null=True, blank=True)
    last_poll = models.BooleanField(null=True, blank=True)
    no_of_terms_held_by_winner = models.FloatField(null=True, blank=True)
    last_party = models.CharField(max_length=100, null=True, blank=True)
    last_party_id = models.IntegerField(null=True, blank=True)
    last_constituency_name = models.CharField(max_length=200, null=True, blank=True)
    same_constituency = models.BooleanField(null=True, blank=True)
    same_party = models.BooleanField(null=True, blank=True)
    no_terms = models.FloatField(null=True, blank=True)
    turncoat = models.BooleanField(null=True, blank=True)
    no_of_turncoat_candidates = models.FloatField(null=True, blank=True)
    pct_of_candidates_turncoat = models.FloatField(null=True, blank=True)
    incumbent = models.BooleanField(null=True, blank=True)
    recontest = models.BooleanField(null=True, blank=True)
    no_of_recontesting_candidates = models.FloatField(null=True, blank=True)
    pct_of_candidates_recontesting = models.FloatField(null=True, blank=True)
    myneta_education = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main_desc = models.CharField(max_length=255, null=True, blank=True)
    tcpd_prof_second = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_second_desc = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'assembly_no', 'constituency_no', 'position']
        verbose_name = 'Election Vidhan Sabha Winners'
        unique_together = ['year', 'assembly_no', 'constituency_no', 'poll_no', 'position', 'candidate']

    def __str__(self):
        return f"Vidhan Sabha Election Winners - {self.year} - {self.assembly_no}/{self.constituency_no} - {self.candidate}"


class VidhanSabhaNOTAResults(models.Model):
    """Vidhan Sabha NOTA data (sheet: nota)."""

    assembly_no = models.IntegerField(db_index=True)
    constituency_no = models.IntegerField(db_index=True)
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(null=True, blank=True)
    delim_id = models.IntegerField(null=True, blank=True)
    poll_no = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    candidate = models.CharField(max_length=255, db_index=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    party = models.CharField(max_length=100, db_index=True)
    votes = models.FloatField(null=True, blank=True)
    age_of_winner = models.FloatField(null=True, blank=True)
    average_age_of_contestants = models.FloatField(null=True, blank=True)
    candidate_type = models.CharField(max_length=50, null=True, blank=True)
    no_of_valid_votes_casted = models.FloatField(null=True, blank=True)
    no_of_electors = models.FloatField(null=True, blank=True)
    select_constituency = models.CharField(max_length=200, db_index=True)
    constituency_type = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    district = models.CharField(max_length=100, db_index=True)
    sub_region = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    no_of_candidates = models.FloatField(null=True, blank=True)
    turnout_rate = models.FloatField(null=True, blank=True)
    vote_share = models.FloatField(null=True, blank=True)
    deposit_lost = models.CharField(max_length=20, null=True, blank=True)
    winning_margin = models.FloatField(null=True, blank=True)
    winning_margin_percentage = models.FloatField(null=True, blank=True)
    enop = models.FloatField(null=True, blank=True)
    pid = models.CharField(max_length=50, null=True, blank=True)
    party_type_tcpd = models.CharField(max_length=100, null=True, blank=True)
    party_id = models.IntegerField(null=True, blank=True)
    last_poll = models.BooleanField(null=True, blank=True)
    no_of_terms_held_by_winner = models.FloatField(null=True, blank=True)
    last_party = models.CharField(max_length=100, null=True, blank=True)
    last_party_id = models.IntegerField(null=True, blank=True)
    last_constituency_name = models.CharField(max_length=200, null=True, blank=True)
    same_constituency = models.BooleanField(null=True, blank=True)
    same_party = models.BooleanField(null=True, blank=True)
    no_terms = models.FloatField(null=True, blank=True)
    turncoat = models.BooleanField(null=True, blank=True)
    no_of_turncoat = models.FloatField(null=True, blank=True)
    pct_of_turncoats = models.FloatField(null=True, blank=True)
    incumbent = models.BooleanField(null=True, blank=True)
    recontest = models.BooleanField(null=True, blank=True)
    no_of_recontests = models.FloatField(null=True, blank=True)
    pct_of_recontests = models.FloatField(null=True, blank=True)
    myneta_education = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main_desc = models.CharField(max_length=255, null=True, blank=True)
    tcpd_prof_second = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_second_desc = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'assembly_no', 'constituency_no', 'position']
        verbose_name = 'Election Vidhan Sabha NOTA Results'
        unique_together = ['year', 'assembly_no', 'constituency_no', 'poll_no', 'position', 'candidate']

    def __str__(self):
        return f"Vidhan Sabha NOTA Results - {self.year} - {self.assembly_no}/{self.constituency_no}"


class LokSabhaElectionWinners(models.Model):
    """Lok Sabha winners data (sheet: First)."""

    assembly_no = models.IntegerField(db_index=True)
    constituency_no = models.IntegerField(db_index=True)
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(null=True, blank=True)
    poll_no = models.IntegerField(null=True, blank=True)
    delim_id = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    candidate = models.CharField(max_length=255, db_index=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    party = models.CharField(max_length=100, db_index=True)
    votes = models.FloatField(null=True, blank=True)
    candidate_type = models.CharField(max_length=50, null=True, blank=True)
    no_of_valid_votes_casted = models.FloatField(null=True, blank=True)
    no_of_registered_electors = models.FloatField(null=True, blank=True)
    select_constituency = models.CharField(max_length=200, db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    constituency_type = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    sub_region = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    no_of_candidates = models.FloatField(null=True, blank=True)
    turnout_rate = models.FloatField(null=True, blank=True)
    vote_share = models.FloatField(null=True, blank=True)
    deposit_lost = models.CharField(max_length=20, null=True, blank=True)
    winning_margin = models.FloatField(null=True, blank=True)
    winning_margin_percentage = models.FloatField(null=True, blank=True)
    enop = models.FloatField(null=True, blank=True)
    pid = models.CharField(max_length=50, null=True, blank=True)
    party_type_tcpd = models.CharField(max_length=100, null=True, blank=True)
    party_id = models.IntegerField(null=True, blank=True)
    last_poll = models.BooleanField(null=True, blank=True)
    contested = models.BooleanField(null=True, blank=True)
    last_party = models.CharField(max_length=100, null=True, blank=True)
    last_party_id = models.IntegerField(null=True, blank=True)
    last_constituency_name = models.CharField(max_length=200, null=True, blank=True)
    same_constituency = models.BooleanField(null=True, blank=True)
    same_party = models.BooleanField(null=True, blank=True)
    no_of_terms_held_by_winner = models.FloatField(null=True, blank=True)
    turncoat = models.BooleanField(null=True, blank=True)
    no_of_turncoat_candidates = models.FloatField(null=True, blank=True)
    pct_of_candidates_turncoat = models.FloatField(null=True, blank=True)
    incumbent = models.BooleanField(null=True, blank=True)
    recontest = models.BooleanField(null=True, blank=True)
    no_of_recontesting_candidates = models.FloatField(null=True, blank=True)
    pct_of_candidates_recontesting = models.FloatField(null=True, blank=True)
    myneta_education = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main_desc = models.CharField(max_length=255, null=True, blank=True)
    tcpd_prof_second = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_second_desc = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'assembly_no', 'constituency_no', 'position']
        verbose_name = 'Election Lok Sabha Winners'
        unique_together = ['year', 'assembly_no', 'constituency_no', 'poll_no', 'position', 'candidate']

    def __str__(self):
        return f"Lok Sabha Election Winners - {self.year} - {self.assembly_no}/{self.constituency_no} - {self.candidate}"


class LokSabhaNOTAResults(models.Model):
    """Lok Sabha NOTA data (sheet: NOTA)."""

    assembly_no = models.IntegerField(db_index=True)
    constituency_no = models.IntegerField(db_index=True)
    year = models.IntegerField(db_index=True)
    month = models.IntegerField(null=True, blank=True)
    poll_no = models.IntegerField(null=True, blank=True)
    delim_id = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    candidate = models.CharField(max_length=255, db_index=True)
    sex = models.CharField(max_length=10, null=True, blank=True)
    party = models.CharField(max_length=100, db_index=True)
    votes = models.FloatField(null=True, blank=True)
    candidate_type = models.CharField(max_length=50, null=True, blank=True)
    valid_votes = models.FloatField(null=True, blank=True)
    electors = models.FloatField(null=True, blank=True)
    select_constituency = models.CharField(max_length=200, db_index=True)
    district = models.CharField(max_length=100, db_index=True)
    constituency_type = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    sub_region = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    n_cand = models.FloatField(null=True, blank=True)
    turnout_percentage = models.FloatField(null=True, blank=True)
    vote_share = models.FloatField(null=True, blank=True)
    deposit_lost = models.CharField(max_length=20, null=True, blank=True)
    margin = models.FloatField(null=True, blank=True)
    margin_percentage = models.FloatField(null=True, blank=True)
    enop = models.FloatField(null=True, blank=True)
    pid = models.CharField(max_length=50, null=True, blank=True)
    party_type_tcpd = models.CharField(max_length=100, null=True, blank=True)
    party_id = models.IntegerField(null=True, blank=True)
    last_poll = models.BooleanField(null=True, blank=True)
    contested = models.BooleanField(null=True, blank=True)
    last_party = models.CharField(max_length=100, null=True, blank=True)
    last_party_id = models.IntegerField(null=True, blank=True)
    last_constituency_name = models.CharField(max_length=200, null=True, blank=True)
    same_constituency = models.BooleanField(null=True, blank=True)
    same_party = models.BooleanField(null=True, blank=True)
    no_terms = models.FloatField(null=True, blank=True)
    turncoat = models.BooleanField(null=True, blank=True)
    incumbent = models.BooleanField(null=True, blank=True)
    recontest = models.BooleanField(null=True, blank=True)
    myneta_education = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_main_desc = models.CharField(max_length=255, null=True, blank=True)
    tcpd_prof_second = models.CharField(max_length=100, null=True, blank=True)
    tcpd_prof_second_desc = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['district', 'year', 'assembly_no', 'constituency_no', 'position']
        verbose_name = 'Election Lok Sabha NOTA Results'
        unique_together = ['year', 'assembly_no', 'constituency_no', 'poll_no', 'position', 'candidate']

    def __str__(self):
        return f"Lok Sabha NOTA Results - {self.year} - {self.assembly_no}/{self.constituency_no}"