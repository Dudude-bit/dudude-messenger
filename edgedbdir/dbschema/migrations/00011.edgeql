CREATE MIGRATION m1blg6xdmbrbe3zl3bypmrh6xgy4gtt7oenvjczcuz7ayi4dw4zjeq
    ONTO m1rbki7cozk22j2wrleejr4noxykywc2ynu26yl7v4c4jpjix5bl7a
{
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY is_active -> std::bool {
          SET default := false;
      };
  };
};
