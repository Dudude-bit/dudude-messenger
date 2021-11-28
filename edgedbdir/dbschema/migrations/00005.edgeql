CREATE MIGRATION m1mehnm3kftsofva7osmpgt3rja535bkgfxvnxcgqzaintbifq4d2a
    ONTO m1ca3bn5zcyw7mrjqdnzd42fk4rhc6gwu5jwp3l6vhdm5o5tuc37jq
{
  CREATE TYPE default::PasswordRecovery {
      CREATE REQUIRED PROPERTY created_at -> std::datetime;
      CREATE REQUIRED PROPERTY expires -> std::duration;
      CREATE REQUIRED PROPERTY expires_at := ((.created_at + .expires));
      CREATE REQUIRED PROPERTY token -> std::uuid {
          SET readonly := true;
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE default::Token {
      ALTER LINK user {
          SET readonly := true;
      };
      ALTER PROPERTY value {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
