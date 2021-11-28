CREATE MIGRATION m1ca3bn5zcyw7mrjqdnzd42fk4rhc6gwu5jwp3l6vhdm5o5tuc37jq
    ONTO m15vk2zijsucsvsq6zqrq6kit3thygyp3rycmkmou2pkzlyr5greja
{
  ALTER TYPE default::Token {
      ALTER LINK to {
          RENAME TO user;
      };
  };
  ALTER TYPE default::User {
      CREATE LINK token := (.<user[IS default::Token]);
  };
};
