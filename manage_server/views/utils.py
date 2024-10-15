from config import Config
import jwt


def get_user_id_from_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"], "成功获取id"
    except jwt.ExpiredSignatureError:
        return None, "Token 已过期"
    except jwt.InvalidTokenError:
        return None, "无效的 Token"
