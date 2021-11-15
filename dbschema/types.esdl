
module default {
    scalar type email extending str {
        constraint regexp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    }
}