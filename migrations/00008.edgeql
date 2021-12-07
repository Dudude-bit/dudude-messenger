CREATE MIGRATION m1njexlmbcuajzngd2lfjkd67iif3joor5ukc3wgsnejz73olragda
    ONTO m1lrhewhdwahrxf3pjtcxh5wr52baj2nndu7veiunmaehtzctwpsqa
{
  ALTER SCALAR TYPE default::email {
      DROP CONSTRAINT std::regexp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
  };
};
