from bson.objectid import ObjectId

class User:
    def __init__(self, firstName, lastName, email, userType, username, password, mobile=None, gender=None, _id=None):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.userType = userType
        self.username = username
        self.password = password
        self.mobile = mobile
        self.gender = gender
        self._id = str(_id) if _id else None

    def to_dict(self):
        user_dict = {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "userType": self.userType,
            "username": self.username,
            "mobile": self.mobile,
            "gender": self.gender
        }
        if self._id:
            user_dict["_id"] = self._id
        return user_dict

    @staticmethod
    def from_dict(data):
        return User(
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            email=data.get("email"),
            userType=data.get("userType"),
            username=data.get("username"),
            password=data.get("password"),
            mobile=data.get("mobile"),
            gender=data.get("gender"),
            _id=str(data.get("_id")) if data.get("_id") else None
        )