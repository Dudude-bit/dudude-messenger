CREATE MIGRATION m1lrhewhdwahrxf3pjtcxh5wr52baj2nndu7veiunmaehtzctwpsqa
    ONTO m1lzl7sgxrzoxgtn3xiutjntshxmmn364t5jdqoo3c4apqvo7263va
{
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY activation_code -> std::uuid {
          SET readonly := true;
          SET REQUIRED USING (SELECT
              <std::uuid>'ff3166cf-19ba-42b1-b4cf-c3bf275d22f8'
          );
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
