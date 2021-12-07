CREATE MIGRATION m1utidiwebv52ghd7ssryoyjswfgkbugfzvrlaa22z7boyp452sbfq
    ONTO initial
{
  CREATE SCALAR TYPE default::email EXTENDING std::str {
      CREATE CONSTRAINT std::regexp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
  };
  CREATE TYPE default::User {
      CREATE REQUIRED PROPERTY created_at -> std::datetime;
      CREATE PROPERTY deleted_at -> std::datetime;
      CREATE REQUIRED PROPERTY email -> default::email {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY username -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::Chat {
      CREATE REQUIRED MULTI LINK members -> default::User {
          CREATE PROPERTY role -> std::str;
      };
      CREATE REQUIRED PROPERTY created_at -> std::datetime;
      CREATE PROPERTY deleted_at -> std::datetime;
      CREATE REQUIRED PROPERTY type -> std::str {
          CREATE CONSTRAINT std::one_of('private', 'group', 'channel');
      };
  };
  CREATE TYPE default::Messenge {
      CREATE REQUIRED LINK to -> default::Chat;
      CREATE REQUIRED LINK from -> default::User;
      CREATE REQUIRED PROPERTY body -> std::str;
      CREATE REQUIRED PROPERTY created_at -> std::datetime;
      CREATE PROPERTY deleted_at -> std::datetime;
  };
};
