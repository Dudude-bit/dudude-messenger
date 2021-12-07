CREATE MIGRATION m1rbki7cozk22j2wrleejr4noxykywc2ynu26yl7v4c4jpjix5bl7a
    ONTO m1p5tqa5gdz6seazeh537yzbrp3nuw6z7o4lyck4wp4nzcc7vc5d2a
{
  ALTER TYPE default::PasswordRecovery {
      ALTER LINK user {
          ON TARGET DELETE  DELETE SOURCE;
      };
  };
};
