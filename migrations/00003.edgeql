CREATE MIGRATION m15vk2zijsucsvsq6zqrq6kit3thygyp3rycmkmou2pkzlyr5greja
    ONTO m1jwdcreyrmkufufr4p7mwmjyfawqj4rrkeu7cms3bpoxu7rrxegka
{
  ALTER TYPE default::Chat {
      CREATE PROPERTY name -> std::str;
  };
  ALTER TYPE default::Token {
      ALTER LINK to {
          ON TARGET DELETE  DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
