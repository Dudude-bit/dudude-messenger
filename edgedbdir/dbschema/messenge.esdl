
module default {
    type Messenge {
        required property created_at -> datetime{
            readonly := true;
        };
        property deleted_at -> datetime;
        required link from -> User;
        required link to -> Chat;
        required property body -> str;
    }
}