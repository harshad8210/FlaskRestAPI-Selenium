import json
from flask_restx import Namespace, Resource, fields, marshal

from VahanApp import driver_dict
from VahanApp.VahanFlaskSelenium.scrapper import scrapper, GeneralException
from VahanApp.VahanFlaskSelenium.model import SearchCount
from VahanApp.VahanFlaskSelenium.utils import count_time, get_id_pass, get_cookies_database, get_web_driver
from VahanApp import working_drivers

api = Namespace("Vehicle", description="Vehicle related operations")

"""API model for serializing response data"""
vahan_info_model = api.model(
    'RC Status',
    {
        'registration_number': fields.String(required=True),
        'RC_status': fields.String(required=True),
        'vehicle_class': fields.String(required=True),
        'fuel': fields.String(required=True),
        'emission_norms': fields.String(required=True),
        'model_name': fields.String(required=True),
        'manufacturer_name': fields.String(required=True),
        'registering_authority': fields.String(required=True),
        'owner_name': fields.String(required=True),
        'registration_date': fields.String(required=True),
        'fitness_regn': fields.String(required=True),
        'MV_tax': fields.String(required=True),
        'PUCC': fields.String(required=True),
        'Company_Name': fields.String(required=True),
        'Validity': fields.String(required=True),
        'Policy_Number': fields.String(required=True),
        'Is_Financed': fields.String(required=True),
    }
)


@api.route("/<string:number>")
@api.param("number", "Vehicle Registration Number")
@api.response(404, "Vehicle not found")
class GetVahanInformation(Resource):

    @count_time
    def get(self, number):

        """Search for unused browser"""
        driver_name, browser, working_driver = get_web_driver(driver_dict=driver_dict, working_drivers=working_drivers)
        count = 0
        search_count = None
        selenium_cookies = None
        print("\n\n\n", driver_name, "\n\n\n")
        if driver_name != 'New':
            """Get search vehicle count from the database"""
            search_count = SearchCount.get_search_count(driver_name)
            count = search_count.searchCount
            cookies, selenium_cookies = get_cookies_database(driver_name)

        mobile_number, password = get_id_pass()

        try:

            """Call scrapper"""
            data = scrapper(vehicle_number=number, count=count, mobile_number=mobile_number, password=password,
                            cookies=selenium_cookies, browser=browser)
            if driver_name == 'New':
                browser.quit()

            new_count = data.get("Count")
            """Remove working driver from list"""
            if driver_name != 'New':
                working_drivers.remove(driver_name)
                """Update search vehicle count"""
                search_count.update({"searchCount": int(new_count)})

            if int(new_count) == 1 and driver_name != 'New':
                new_cookies = json.loads(data.get("cookies_json"))

                """Update Cookies to database"""
                for db_cookie in range(len(cookies)):
                    new_cookie = {
                        "domain": new_cookies[db_cookie].get("domain"),
                        "httpOnly": new_cookies[db_cookie].get("httpOnly"),
                        "name": new_cookies[db_cookie].get("name"),
                        "path": new_cookies[db_cookie].get("path"),
                        "sameSite": new_cookies[db_cookie].get("sameSite"),
                        "secure": new_cookies[db_cookie].get("secure"),
                        "value": new_cookies[db_cookie].get("value")
                    }
                    cookies[db_cookie].update(new_cookie)

            data = marshal(data, vahan_info_model)
        except GeneralException as error:
            if driver_name != 'New':
                working_drivers.remove(driver_name)
            data = {'Error': str(error)}
            status_code = 400
            return data, status_code
        return data
