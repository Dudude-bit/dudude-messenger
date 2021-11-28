
module default {
    type Token {
        required property created_at -> datetime{
            readonly := true;
        };
        property expiring -> duration;
        required link user -> User{
            constraint exclusive;
            on target delete delete source;
            readonly := true;
        };
        required property value -> uuid {
            constraint exclusive;
            readonly := true;
        };
    }
}