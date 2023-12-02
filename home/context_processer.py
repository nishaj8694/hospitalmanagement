from docter.models import DoctorProfile
from patient.models import patientProfile

def profile_picture(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:  # Check if the user is an admin
            profile_picture_url = None
            docter_available=None
            docter_id=None
            profile_verfy_check=None
        elif request.user.is_docter:
            person=DoctorProfile.objects.get(user_id=request.user.id)   # Check if the user is a staff/user
            profile_picture_url = person.image
            docter_available=person.is_available
            docter_id=person.id
            profile_verfy_check=person.is_verify
        else:
            person=patientProfile.objects.get(user_id=request.user.id)                          # For other users (client, for instance)
            profile_picture_url = person.image
            docter_available=None
            docter_id=None
            profile_verfy_check=person.is_verify

    else:
        profile_picture_url = None  # Or set a default picture for non-authenticated users
        docter_available=None
        docter_id=None
        profile_verfy_check=None
    return {
        'profile_picture_url': profile_picture_url,'profile_verfy_check':profile_verfy_check,
        'docter_available':docter_available,'docter_id':docter_id
    }