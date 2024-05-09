from flask_restx import Api

from VahanApp.VahanFlaskSelenium.vehicle import api as vahan_api

api = Api(
    title="Vehicle API",
    version="1.0",
    description="Get vehicle information from Vahan",
)

api.add_namespace(vahan_api)
