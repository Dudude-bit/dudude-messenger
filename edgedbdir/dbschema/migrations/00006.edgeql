CREATE MIGRATION m1lzl7sgxrzoxgtn3xiutjntshxmmn364t5jdqoo3c4apqvo7263va
    ONTO m1mehnm3kftsofva7osmpgt3rja535bkgfxvnxcgqzaintbifq4d2a
{
  ALTER TYPE default::PasswordRecovery {
      CREATE REQUIRED LINK user -> default::User {
          SET REQUIRED USING (SELECT
              default::User
          FILTER
              (.email = 'test@test.com')
          );
      };
  };
};
