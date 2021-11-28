CREATE MIGRATION m1jwdcreyrmkufufr4p7mwmjyfawqj4rrkeu7cms3bpoxu7rrxegka
    ONTO m1utidiwebv52ghd7ssryoyjswfgkbugfzvrlaa22z7boyp452sbfq
{
  ALTER TYPE default::Chat {
      ALTER PROPERTY created_at {
          SET readonly := true;
      };
  };
  ALTER TYPE default::Messenge {
      ALTER PROPERTY created_at {
          SET readonly := true;
      };
  };
  CREATE TYPE default::Token {
      CREATE REQUIRED LINK to -> default::User;
      CREATE REQUIRED PROPERTY created_at -> std::datetime {
          SET readonly := true;
      };
      CREATE PROPERTY expiring -> std::duration;
      CREATE REQUIRED PROPERTY value -> std::uuid {
          SET readonly := true;
      };
  };
  ALTER TYPE default::User {
      ALTER PROPERTY created_at {
          SET readonly := true;
      };
  };
};
