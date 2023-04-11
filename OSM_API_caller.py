import requests

''''

ideen er at bruge dette kald:

[out:csv(::id, "name:en")];
relation["admin_level"="2"]["boundary"="administrative"]
["ISO3166-1"~"^(AD|AL|AT|BA|BE|BG|BY|CH|CY|CZ|DE|DK|EE|ES|FI|FR|GB|GR|HR|HU|IE|IS|IT|LI|LT|LU|LV|MC|MD|ME|MK|MT|NL|NO|PL|PT|RO|RS|RU|SE|SI|SK|SM|UA|VA)$"];
out;

Til at generere en csv fil med alle de lande OSM har data for i europa.
Derefter kan vi bruge ID'erne til at hente data for de enkelte lande.

'''

def download_osm_data(country_id):
    # Define the API endpoint URL and the filename for the output XML file
    endpoint_url = "https://www.openstreetmap.org/api/0.6/relation/{}.xml".format(country_id)
    output_filename = "{}.xml".format(country_id)

    # Make the API request and get the response content as bytes
    response = requests.get(endpoint_url)
    response_content = response.content

    # Write the response content to the output file
    with open(output_filename, "wb") as output_file:
        output_file.write(response_content)

    print("OpenStreetMap data for country ID {} downloaded and saved to file {}".format(country_id, output_filename))

if __name__ == '__main__':

    print("Calling api to get list of countries:")



