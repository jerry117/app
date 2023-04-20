from flask import jsonify, request, current_app, url_for, g
from flask.views import MethodView

from app.todoism.apis.v1 import api_v1
from app.todoism.apis.v1.auth import auth_required
from app.todoism.apis.v1.errors import api_abort, ValidationError
from app.extensions import db
from app.todoism.models import User, Item
from app.todoism.apis.v1.schemas import user_schema, item_schema, items_schema


def get_item_body():
    data = request.get_json()
    body = data.get('body')
    if body is None or str(body).strip() == '':
        raise ValidationError('The item body was empty or invalid.')
    return body

class IndexAPI(MethodView):

    def get(self):
        return jsonify({
            "api_version": "1.0",
            "api_base_url": "http://example.com/api/v1",
            "current_user_url": "http://example.com/api/v1/user",
            "authentication_url": "http://example.com/api/v1/token",
            "item_url": "http://example.com/api/v1/items/{item_id }",
            "current_user_items_url": "http://example.com/api/v1/user/items{?page,per_page}",
            "current_user_active_items_url": "http://example.com/api/v1/user/items/active{?page,per_page}",
            "current_user_completed_items_url": "http://example.com/api/v1/user/items/completed{?page,per_page}",
        })


class ItemAPI(MethodView):
    decorators = [auth_required]

    def get(self, item_id):
        """Get item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        return jsonify(item_schema(item))

    def put(self, item_id):
        """Edit item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        item.body = get_item_body()
        db.session.commit()
        return '', 204

    def patch(self, item_id):
        """Toggle item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        item.done = not item.done
        db.session.commit()
        return '', 204

    def delete(self, item_id):
        """Delete item."""
        item = Item.query.get_or_404(item_id)
        if g.current_user != item.author:
            return api_abort(403)
        db.session.delete(item)
        db.session.commit()
        return '', 204
    
api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])
# api_v1.add_url_rule('/oauth/token', view_func=AuthTokenAPI.as_view('token'), methods=['POST'])
# api_v1.add_url_rule('/user', view_func=UserAPI.as_view('user'), methods=['GET'])
# api_v1.add_url_rule('/user/items', view_func=ItemsAPI.as_view('items'), methods=['GET', 'POST'])
# api_v1.add_url_rule('/user/items/<int:item_id>', view_func=ItemAPI.as_view('item'), methods=['GET', 'PUT', 'PATCH', 'DELETE'])
# api_v1.add_url_rule('/user/items/active', view_func=ActiveItemsAPI.as_view('active_items'), methods=['GET'])
# api_v1.add_url_rule('/user/items/completed', view_func=CompletedItemsAPI.as_view('completed_items'), methods=['GET', 'DELETE'])