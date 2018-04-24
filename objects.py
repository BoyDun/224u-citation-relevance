# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import collections

import bs4

## JudicialOpinion ###################################################################################################

class JudicialOpinion(object):
    
    def __init__(self, identifier, html, paragraphs): # TODO: later accept datetime as (potentially optional) constructor arg, but for now don't want to mess up cache loading
        self.identifier = identifier
        self.html = html
        self.paragraphs = paragraphs
        self.datetime = None
    
    def plain_text(self):
        return bs4.BeautifulSoup(self.html, "html5lib").get_text().strip()
            
    def extract_cited_opinion_identifiers(self):
        return regex_extraction.citations.OptionalNameAndCitationRegex.generic().findall(self.html)
   
    def extract_citations(self):
        opinion_identifiers = regex_extraction.citations.CitationRegex.generic().findall(self.html)
        citations = set()
        for identifier in opinion_identifiers:
            citations.update(identifier.citations)
        return list(citations)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return "JudicialOpinion(%s)" % (self.identifier)

    def __eq__(self, other):
        return self.identifier == other.identifier

## CourtListenerOpinion

class CourtListenerOpinion(JudicialOpinion):

    def __init__(self, identifier, html, paragraphs, raw_json_object):
        self.raw_json_object = raw_json_object
        super(CourtListenerOpinion, self).__init__(identifier, html, paragraphs)

    def extract_cited_court_listener_ids(self):
        court_listener_ids = []
        for link in self.raw_json_objet["opinions_cited"]:
            court_listener_ids.append(CourtListenerLinkRegex().search(link))
        return court_listener_ids


## Citation ########################################################################################################

class Citation(object):

    def __init__(self, volume, reporter, page):
        self._volume = volume if volume is None or len(volume) > 0 else None
        self._reporter = reporter if reporter is None or len(reporter) > 0 else None
        self._page = page if page is None or len(page) > 0 else None
    
    def get_volume(self):
        return self._volume
    
    def get_reporter(self):
        return self._reporter
    
    def get_page(self):
        return self._page
    
    def to_tuple(self):
        return (self.get_volume(), self.get_reporter(), self.get_page())
    
    def is_valid(self):
        return self._volume is not None and self._reporter is not None and self._page is not None

    def __eq__(self, other):
        if not self.is_valid() or not other.is_valid():
            return False
        if self._volume != other._volume:
            return False
        if self._reporter != other._reporter:
            return False
        if self._page != other._page:
            return False
        return True

    def __hash__(self):
        return hash((self._volume, self._reporter, self._page))

    def __repr__(self):
        return "%s(%s %s %s)" % (self.__class__.__name__, self._volume, self._reporter, self._page)

    def to_plain_text(self):
        return " ".join([self._volume, self._reporter, self._page])

class OpinionIdentifier(object):
   
    def __init__(self):
        self.numerical_identifier_map = {}
        self.jurisdiction = None
        self.citations = []
        self.case_names = []
        self.year = None
        self.court_listener_url = None
        self.jurisdiction_type = None

    def set_numerical_identifier(self, data_set_name, numerical_identifier):
        if self.is_value_valid(numerical_identifier):
            self.numerical_identifier_map[data_set_name] = numerical_identifier
    
    def get_numerical_identifier(self, data_set_name):
        if data_set_name in self.numerical_identifier_map:
            return self.numerical_identifier_map[data_set_name]
        else:
            return None

    def do_numerical_idenfiers_conflict(self, other_identifier):
        for data_set_name in constants.DataSetName.PRECEDENCE_ORDER:
            numerical_identifier = self.get_numerical_identifier(data_set_name)
            other_numerical_identifier = other_identifier.get_numerical_identifier(data_set_name)
            if self.is_value_valid(numerical_identifier):
                if self.is_value_valid(other_numerical_identifier):
                    return numerical_identifier != other_numerical_identifier
        return False

    def set_jurisdiction(self, jurisdiction):
        if self.is_value_valid(jurisdiction):
            self.jurisdiction = jurisdiction

    def do_jurisdictions_conflict(self, other_opinion_identifier):
        if self.is_value_valid(self.jurisdiction):
            if self.is_value_valid(other_opinion_identifier.jurisdiction):
                return self.jurisdiction != other_opinion_identifier.jurisdiction
        return False
    
    def set_jurisdiction_type(self, jurisdiction_type):
        if jurisdiction_type is not None:
            self.jurisdiction_type = jurisdiction_type

    def add_citation(self, citation):
        if self.is_value_valid(citation.get_volume()) and self.is_value_valid(citation.get_reporter()) and self.is_value_valid(citation.get_page()):
            citations = set(self.citations)
            citations.add(citation)
            self.citations = list(citations)
                
    def add_case_name(self, case_name):
        if self.is_value_valid(case_name):
            case_names = set(self.case_names)
            case_names.add(case_name)
            self.case_names = list(case_names)

    def get_longest_case_name(self):
        if len(self.case_names) == 0: return None
        else: return max(self.case_names, key=lambda case_name: len(case_name))

    def set_year(self, year):
        if self.is_value_valid(year):
            self.year = year

    def do_years_conflict(self, other_opinion_identifier):
        if self.is_value_valid(self.year):
            if self.is_value_valid(other_opinion_identifier.year):
                return self.year != other_opinion_identifier.year
        return False

    def set_court_listener_url(self, court_listener_url):
        if self.is_value_valid(court_listener_url):
            self.court_listener_url = court_listener_url

    def do_court_listener_urls_conflict(self, other_opinion_identifier):
        if self.is_value_valid(self.court_listener_url):
            if self.is_value_valid(other_opinion_identifier.court_listener_url):
                return self.court_listener_url != other_opinion_identifier.court_listener_url
        return False

    def __repr__(self):
        case_name = self.get_longest_case_name()
        case_name = "" if case_name is None else util.str_.aggressivelySanitize(case_name)
        return "%s(jurisdiction=%s, name=%s, identifiers=%s, citations=%s)" % (self.__class__.__name__, self.jurisdiction, case_name, self.numerical_identifier_map, self.citations)
    
    def __eq__(self, other):
        return str(self) == str(other)

    @classmethod
    def is_value_valid(cls, numerical_identifier):
        return numerical_identifier is not None and len(numerical_identifier) > 0
    
    def does_conflict(self, other_identifier):
        return sum([
            self.do_numerical_idenfiers_conflict(other_identifier),
            self.do_jurisdictions_conflict(other_identifier),
            self.do_years_conflict(other_identifier),
            self.do_court_listener_urls_conflict(other_identifier),
        ]) > 0

    @classmethod
    def combine(cls, identifiers):
        assert(len(identifiers) > 0)
        
        identifier = identifiers[0]
        for additional_identifier in identifiers[1:]:
            if not identifier.does_conflict(additional_identifier):
                # We don't worry about overwriting since we've already checked to ensure both are equivalent if valid.
                
                # Combine numerical identifiers:
                for data_set_name in constants.DataSetName.PRECEDENCE_ORDER:
                    identifier.set_numerical_identifier(data_set_name, additional_identifier.get_numerical_identifier(data_set_name))
        
                # Combine jurisdictions:
                identifier.set_jurisdiction(additional_identifier.jurisdiction)
                
                # Combine citations:
                for citation in additional_identifier.citations:
                    identifier.add_citation(citation)
                
                # Combine case names:
                for case_name in additional_identifier.case_names:
                    identifier.add_case_name(case_name)

                # Combine years:
                identifier.set_year(additional_identifier.year)

                # Combine CourtListener urls:
                identifier.set_court_listener_url(additional_identifier.court_listener_url)

        return identifier

    @classmethod
    def with_citation(cls, citation):
        identifier = cls()
        identifier.add_citation(citation)
        return identifier
