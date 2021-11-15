
module default {
    type Chat {
        required property created_at -> datetime;
        property deleted_at -> datetime;
        required property type -> str {
          constraint one_of ('private', 'group', 'channel')
        };
        required multi link members -> User {
            property role -> str;

        }
    }
}