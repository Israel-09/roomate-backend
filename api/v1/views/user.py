from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models.recommendations.find_similarity import get_top_matches
from api.v1.auth.auth import Auth

AUTH = Auth()
@app_views.route('/finder', methods=['GET'], strict_slashes=False)
def recommend_roomate() -> str:
    """ 
    Return:
      - list of all User match
    """
    session_id = request.cookies.get('session_id')
    print(session_id)
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user:
        matches = get_top_matches(user.id)
        matches_profile = []
        for match in matches:
            m_id, m_com = int(match.get('user_id')), int(match.get('compatibility'))
            person = AUTH.get_user_from_id(m_id)
            profile = {
                    'name': f'{person.profile.last_name} {person.profile.first_name}',
                    'compatibility': m_com
            }
            matches_profile.append(profile)
        return jsonify({"user_id": user.id, "match":matches_profile})
    abort(403)
