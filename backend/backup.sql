--
-- PostgreSQL database dump
--

\restrict ZGg1sG0LLHQ3PZoR69fpXr8NH8oNL3A5UHhFDAjnUWjvzE4RwaOw0QLemcgYsOE

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: study_activity; Type: TABLE; Schema: public; Owner: medha
--

CREATE TABLE public.study_activity (
    id integer NOT NULL,
    activity_date date NOT NULL
);


ALTER TABLE public.study_activity OWNER TO medha;

--
-- Name: study_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: medha
--

CREATE SEQUENCE public.study_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.study_activity_id_seq OWNER TO medha;

--
-- Name: study_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medha
--

ALTER SEQUENCE public.study_activity_id_seq OWNED BY public.study_activity.id;


--
-- Name: subjects; Type: TABLE; Schema: public; Owner: medha
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    name text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.subjects OWNER TO medha;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: medha
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_id_seq OWNER TO medha;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medha
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: topics; Type: TABLE; Schema: public; Owner: medha
--

CREATE TABLE public.topics (
    id integer NOT NULL,
    unit_id integer NOT NULL,
    name text NOT NULL,
    status text NOT NULL,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT topics_status_check CHECK ((status = ANY (ARRAY['Not Started'::text, 'In Progress'::text, 'Completed'::text])))
);


ALTER TABLE public.topics OWNER TO medha;

--
-- Name: topics_id_seq; Type: SEQUENCE; Schema: public; Owner: medha
--

CREATE SEQUENCE public.topics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.topics_id_seq OWNER TO medha;

--
-- Name: topics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medha
--

ALTER SEQUENCE public.topics_id_seq OWNED BY public.topics.id;


--
-- Name: unit_notes; Type: TABLE; Schema: public; Owner: medha
--

CREATE TABLE public.unit_notes (
    id integer NOT NULL,
    unit_id integer,
    content text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.unit_notes OWNER TO medha;

--
-- Name: unit_notes_id_seq; Type: SEQUENCE; Schema: public; Owner: medha
--

CREATE SEQUENCE public.unit_notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.unit_notes_id_seq OWNER TO medha;

--
-- Name: unit_notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medha
--

ALTER SEQUENCE public.unit_notes_id_seq OWNED BY public.unit_notes.id;


--
-- Name: units; Type: TABLE; Schema: public; Owner: medha
--

CREATE TABLE public.units (
    id integer NOT NULL,
    subject_id integer NOT NULL,
    name text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.units OWNER TO medha;

--
-- Name: units_id_seq; Type: SEQUENCE; Schema: public; Owner: medha
--

CREATE SEQUENCE public.units_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.units_id_seq OWNER TO medha;

--
-- Name: units_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: medha
--

ALTER SEQUENCE public.units_id_seq OWNED BY public.units.id;


--
-- Name: study_activity id; Type: DEFAULT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.study_activity ALTER COLUMN id SET DEFAULT nextval('public.study_activity_id_seq'::regclass);


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- Name: topics id; Type: DEFAULT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.topics ALTER COLUMN id SET DEFAULT nextval('public.topics_id_seq'::regclass);


--
-- Name: unit_notes id; Type: DEFAULT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.unit_notes ALTER COLUMN id SET DEFAULT nextval('public.unit_notes_id_seq'::regclass);


--
-- Name: units id; Type: DEFAULT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.units ALTER COLUMN id SET DEFAULT nextval('public.units_id_seq'::regclass);


--
-- Data for Name: study_activity; Type: TABLE DATA; Schema: public; Owner: medha
--

COPY public.study_activity (id, activity_date) FROM stdin;
\.


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: medha
--

COPY public.subjects (id, name, created_at) FROM stdin;
1	Data Structures	2025-12-17 11:05:00.152779
2	DBMS	2025-12-17 11:05:00.152779
3	Fundamentals of Cyber Security	2025-12-17 15:47:09.090818
4	DAA	2026-01-09 12:41:09.181733
\.


--
-- Data for Name: topics; Type: TABLE DATA; Schema: public; Owner: medha
--

COPY public.topics (id, unit_id, name, status, updated_at) FROM stdin;
23	6	Aggregate functions	Completed	2025-12-18 17:07:56.624293
21	6	joins	Not Started	2025-12-18 17:23:20.686258
20	6	DCL	Not Started	2025-12-18 17:23:21.269933
19	6	TCL	Not Started	2025-12-18 17:23:22.011462
18	6	DML	Not Started	2025-12-18 17:23:22.540711
17	6	DDL	Not Started	2025-12-18 17:23:23.020239
22	6	Subqueries	Completed	2025-12-22 15:20:23.152494
13	5	Schemas	Not Started	2026-01-09 12:44:12.824965
14	5	2 tier and 3 tier Architecture	Completed	2026-01-09 12:44:13.332002
16	5	ACID Properties	Not Started	2026-01-09 12:44:14.576528
15	5	Advantages of DBMS	Not Started	2026-01-09 12:44:15.45249
12	5	Types of databases	Not Started	2026-01-09 12:44:17.004744
1	1	Introduction	Not Started	2026-01-09 12:49:51.700942
2	1	Fundamentals	Not Started	2026-01-09 12:49:53.226084
11	1	Summary	Not Started	2026-01-09 12:49:54.090846
3	3	Hackers and their types	Not Started	2026-01-09 13:18:25.005864
\.


--
-- Data for Name: unit_notes; Type: TABLE DATA; Schema: public; Owner: medha
--

COPY public.unit_notes (id, unit_id, content, created_at) FROM stdin;
\.


--
-- Data for Name: units; Type: TABLE DATA; Schema: public; Owner: medha
--

COPY public.units (id, subject_id, name, created_at) FROM stdin;
1	1	Unit 1 Basics	2025-12-17 15:41:10.913577
3	3	Unit 1 Types of Cyberattacks	2025-12-17 16:23:45.965706
5	2	Introduction	2025-12-18 15:29:35.039855
6	2	SQL	2025-12-18 15:30:13.753169
\.


--
-- Name: study_activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: medha
--

SELECT pg_catalog.setval('public.study_activity_id_seq', 1, false);


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: medha
--

SELECT pg_catalog.setval('public.subjects_id_seq', 4, true);


--
-- Name: topics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: medha
--

SELECT pg_catalog.setval('public.topics_id_seq', 23, true);


--
-- Name: unit_notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: medha
--

SELECT pg_catalog.setval('public.unit_notes_id_seq', 3, true);


--
-- Name: units_id_seq; Type: SEQUENCE SET; Schema: public; Owner: medha
--

SELECT pg_catalog.setval('public.units_id_seq', 6, true);


--
-- Name: study_activity study_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.study_activity
    ADD CONSTRAINT study_activity_pkey PRIMARY KEY (id);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: topics topics_pkey; Type: CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_pkey PRIMARY KEY (id);


--
-- Name: unit_notes unit_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.unit_notes
    ADD CONSTRAINT unit_notes_pkey PRIMARY KEY (id);


--
-- Name: units units_pkey; Type: CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT units_pkey PRIMARY KEY (id);


--
-- Name: units fk_subject; Type: FK CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.units
    ADD CONSTRAINT fk_subject FOREIGN KEY (subject_id) REFERENCES public.subjects(id) ON DELETE CASCADE;


--
-- Name: topics fk_unit; Type: FK CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT fk_unit FOREIGN KEY (unit_id) REFERENCES public.units(id) ON DELETE CASCADE;


--
-- Name: unit_notes unit_notes_unit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: medha
--

ALTER TABLE ONLY public.unit_notes
    ADD CONSTRAINT unit_notes_unit_id_fkey FOREIGN KEY (unit_id) REFERENCES public.units(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict ZGg1sG0LLHQ3PZoR69fpXr8NH8oNL3A5UHhFDAjnUWjvzE4RwaOw0QLemcgYsOE

