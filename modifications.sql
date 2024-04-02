CREATE TABLE public.frontier (
    id serial PRIMARY KEY,
    link varchar
);

CREATE INDEX "idx_frontier_id" ON public.frontier ( id );

INSERT INTO public.frontier (link)
VALUES ('https://gov.si/'),
    ('https://evem.gov.si/'),
    ('https://e-uprava.gov.si/'),
    ('https://e-prostor.gov.si/');