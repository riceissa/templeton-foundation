#!/usr/bin/env python3
# License: CC0

import json
from bs4 import BeautifulSoup

def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def main():
    print("""insert into donations (donor, donee, amount, donation_date,
    donation_date_precision, donation_date_basis, cause_area, url,
    donor_cause_area_url, notes, affected_countries,
    affected_regions) values""")

    first = True

    with open("data.json", "r") as f:
        j = json.load(f)

        for row in j:
            (start_year, title_html, project_leaders, grantee, amount,
             funding_area, region) = row

            start_year = int(start_year)

            soup = BeautifulSoup(title_html, "lxml")
            title = soup.text
            # FIXME: This is the URL that describes each grant, which is
            # distinct from the URL for the grants database (which is the same
            # for all grants).  Do we want to use this url?
            url = soup.find("a")["href"]

            soup = BeautifulSoup(project_leaders, "lxml")
            project_leaders = soup.text

            assert amount.startswith("$")
            amount = amount.replace("$", "").replace(",", "")

            print(("    " if first else "    ,") + "(" + ",".join([
                mysql_quote("John Templeton Foundation"),  # donor
                mysql_quote(grantee),  # donee
                amount,  # amount
                mysql_quote(str(start_year) + "-01-01"),  # donation_date
                mysql_quote("year"),  # donation_date_precision
                mysql_quote("donation log"),  # donation_date_basis
                mysql_quote(funding_area),  # cause_area ; FIXME: Templeton uses "funding area" which might not be cause area, so remap this value as necessary
                mysql_quote("https://templeton.org/grants/grant-database"),  # url
                mysql_quote("FIXME"),  # donor_cause_area_url
                mysql_quote("For project " + title + "; " +
                            "Project leaders: " + project_leaders),  # notes
                mysql_quote("FIXME"),  # affected_countries
                mysql_quote(region),  # affected_regions ; FIXME: the region names are {'USA', 'North America', 'South America', 'Africa', 'Oceania', 'Europe', 'Asia'}. We might want to remap this.
            ]) + ")")
            first = False
        print(";")


if __name__ == "__main__":
    main()
