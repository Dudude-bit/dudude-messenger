
module default {
    type User {
        required property created_at -> datetime;
        property deleted_at -> datetime;
        required property username -> str {
            constraint exclusive;
        }
        required property email -> email {
            constraint exclusive;
        }
    }
}