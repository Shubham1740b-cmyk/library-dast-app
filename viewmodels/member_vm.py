"""
VIEWMODEL: Member

Prepares data specifically for member-related views.
Handles both list and form operations.
"""
from models.member import Member


class MemberViewModel:
    @staticmethod
    def get_members_for_list():
        """Get list of members for display in member list view."""
        return Member.all()
    
    @staticmethod
    def get_member_form_data():
        """Get empty form data for creating a new member."""
        return {
            'errors': [],
            'data': {
                'name': '',
                'email': '',
                'roll_no': ''
            }
        }
    
    @staticmethod
    def validate_member_data(name, email, roll_no):
        """Validate member data and return ViewModel-ready format."""
        errors = Member.validate(name, email, roll_no)
        data = {
            'name': name,
            'email': email,
            'roll_no': roll_no
        }
        return {
            'errors': errors,
            'data': data
        }
    
    @staticmethod
    def create_member(name, email, roll_no):
        """Create a new member and return success message."""
        Member.create(name, email, roll_no)
        return f"{name} was registered as a member."
