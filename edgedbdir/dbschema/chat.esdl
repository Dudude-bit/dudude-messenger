
module default {
    type Chat {
        required property created_at -> datetime{
            readonly := true;
        };
        property deleted_at -> datetime;
        required property type -> str {
          constraint one_of ('private', 'group', 'channel')
        };
        property name -> str;
        required multi link members -> User {
            property role -> str;

        }
    }
}