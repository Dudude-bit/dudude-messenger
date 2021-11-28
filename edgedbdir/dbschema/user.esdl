
module default {
    type User {
        required property created_at -> datetime{
            readonly := true;
        };
        property deleted_at -> datetime;
        required property username -> str {
            constraint exclusive;
        };
        required property email -> email {
            constraint exclusive;
        };
        required property activation_code -> uuid {
            readonly := true;
            constraint exclusive;
        };
        link token := .<user[IS Token];
    }
}