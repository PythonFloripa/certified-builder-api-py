from src.domain.response.tech_floripa import TechOrdersResponse
from src.domain.entity.order import Order
from src.domain.entity.product import Product
from src.domain.entity.participant import Participant
from src.domain.entity.certificate import Certificate

class TechOrderMapper:
    @staticmethod
    def to_entity(tech_order_response: TechOrdersResponse) -> Order:
        return Order(
            order_id=tech_order_response.order_id,
            order_date=tech_order_response.order_date,
            participant_first_name=tech_order_response.first_name,
            participant_last_name=tech_order_response.last_name,
            participant_email=tech_order_response.email,
            participant_phone=tech_order_response.phone,
            participant_cpf=tech_order_response.cpf,
            participant_city=tech_order_response.city,
            product_id=tech_order_response.product_id,
            product_name=tech_order_response.product_name,
            certificate_details=tech_order_response.certificate_details,
            certificate_logo=tech_order_response.certificate_logo,
            certificate_background=tech_order_response.certificate_background,
            checkin_latitude=tech_order_response.checkin_latitude,
            checkin_longitude=tech_order_response.checkin_longitude,
            time_checkin=tech_order_response.time_checkin
        )
    
class TechProductMapper:
    @staticmethod
    def to_entity(tech_product_response: TechOrdersResponse) -> Product:
        return Product(
            product_id=tech_product_response.product_id,
            product_name=tech_product_response.product_name,
            certificate_details=tech_product_response.certificate_details,
            certificate_logo=tech_product_response.certificate_logo,
            certificate_background=tech_product_response.certificate_background,
            checkin_latitude=tech_product_response.checkin_latitude,
            checkin_longitude=tech_product_response.checkin_longitude,
            time_checkin=tech_product_response.time_checkin         
        )
    
class TechParticipantMapper:
    @staticmethod
    def to_entity(tech_order_response: TechOrdersResponse) -> Order:
        return Participant(
            first_name=tech_order_response.first_name,
            last_name=tech_order_response.last_name,
            email=tech_order_response.email,
            phone=tech_order_response.phone,
            cpf=tech_order_response.cpf,
            city=tech_order_response.city
        )
    
class CertificateMapper:
    @staticmethod
    def to_entity(tech_order_response: TechOrdersResponse) -> Certificate:
        return Certificate(            
            order_id=tech_order_response.order_id,
            order_date=tech_order_response.order_date,
            product_id=tech_order_response.product_id,
            product_name=tech_order_response.product_name,
            certificate_details=tech_order_response.certificate_details,
            certificate_logo=tech_order_response.certificate_logo,
            certificate_background=tech_order_response.certificate_background,
            participant_email=tech_order_response.email,
            participant_first_name=tech_order_response.first_name,
            participant_last_name=tech_order_response.last_name,
            participant_cpf=tech_order_response.cpf,
            participant_phone=tech_order_response.phone,
            participant_city=tech_order_response.city
        )