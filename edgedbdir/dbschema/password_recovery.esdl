
module default {
    type PasswordRecovery {
        required property created_at -> datetime;
        required property expires -> duration;
        required property expires_at := .created_at + .expires;
        required property token -> uuid {
            constraint exclusive;
            readonly := true;
        };
        required link user -> User;
    }
}