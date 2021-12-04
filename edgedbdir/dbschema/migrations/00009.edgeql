CREATE MIGRATION m1p5tqa5gdz6seazeh537yzbrp3nuw6z7o4lyck4wp4nzcc7vc5d2a
    ONTO m1njexlmbcuajzngd2lfjkd67iif3joor5ukc3wgsnejz73olragda
{
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY password -> std::str {
          SET REQUIRED USING (SELECT
              '123'
          );
      };
  };
};
