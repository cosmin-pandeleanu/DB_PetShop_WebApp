CREATE TABLE categorii_animale (
    id_categorie       TINYINT     NOT NULL AUTO_INCREMENT,
    denumire_categorie VARCHAR(30) NOT NULL,
    CONSTRAINT categorii_animale_pk PRIMARY KEY ( id_categorie )
);
ALTER TABLE categorii_animale
    ADD CONSTRAINT categorii_animale_den_cat_ck CHECK ( 
	( char_length(denumire_categorie) > 3 ) AND ( REGEXP_LIKE ( denumire_categorie, '^[A-Za-zăîâșțĂÎÂȘȚ ]+$' ) ) );
ALTER TABLE categorii_animale ADD CONSTRAINT categorii_animale_denum_cat_un UNIQUE ( denumire_categorie );

CREATE TABLE clienti (
    nr_card     BIGINT       NOT NULL AUTO_INCREMENT ,
    nume_client VARCHAR(40),
    CONSTRAINT clienti_pk PRIMARY KEY ( nr_card )
);
ALTER TABLE clienti
    ADD CONSTRAINT clienti_nume_client_ck CHECK ( 
	( char_length(nume_client) > 3 ) AND ( REGEXP_LIKE ( nume_client,'^[A-Za-zăîâșțĂÎÂȘȚ ]+$' ) ) );
ALTER TABLE clienti ADD CONSTRAINT clienti_nume_client_un UNIQUE ( nume_client );

CREATE TABLE detalii_clienti (
    nr_card       BIGINT       NOT NULL AUTO_INCREMENT,
    email         VARCHAR(50),
    data_nasterii DATETIME,
    gen           CHAR(1),
    adresa        VARCHAR(40),
    oras          VARCHAR(30),
    CONSTRAINT detalii_clienti_pk PRIMARY KEY ( nr_card )
);
ALTER TABLE detalii_clienti
    ADD CONSTRAINT `datelii_clienti_email_ck` CHECK ( REGEXP_LIKE ( email,'[a-z0-9._%-]+@[a-z0-9._%-]+.[a-z]{2,4}' ) );
CREATE UNIQUE INDEX detalii_clienti__idx ON detalii_clienti (nr_card ASC );
ALTER TABLE detalii_clienti ADD CONSTRAINT `detalii_clienti_email_UN` UNIQUE ( email );

CREATE TABLE furnizori (
    id_furnizor       SMALLINT    NOT NULL AUTO_INCREMENT,
    denumire_furnizor VARCHAR(25) NOT NULL,
    CONSTRAINT furnizori_pk PRIMARY KEY ( id_furnizor )
);

ALTER TABLE furnizori
    ADD CONSTRAINT furnizori_denum_furnizor_ck CHECK ( 
	( char_length(denumire_furnizor) > 3 ) AND ( REGEXP_LIKE ( denumire_furnizor, '^[A-Za-zăîâșțĂÎÂȘȚ ]+$' ) ) );
ALTER TABLE furnizori ADD CONSTRAINT furnizori_denumire_furnizor_un UNIQUE ( denumire_furnizor );

CREATE TABLE produse (
    id_produs       BIGINT        NOT NULL AUTO_INCREMENT,
    denumire_produs VARCHAR(30)   NOT NULL,
    stoc            SMALLINT      NOT NULL,
    pret            DECIMAL(7, 2) NOT NULL,
    um              VARCHAR(3)    NOT NULL,
    id_furnizor     SMALLINT      NOT NULL,
    id_categorie    TINYINT		  NOT NULL,
    id_tip          TINYINT       NOT NULL,
    CONSTRAINT produse_pk PRIMARY KEY ( id_produs )
);

ALTER TABLE produse
    ADD CONSTRAINT produse_denumire_produs_ck CHECK ( char_length(denumire_produs) > 2 );
ALTER TABLE produse ADD CONSTRAINT produse_stoc_ck CHECK ( stoc > 0 );
ALTER TABLE produse ADD CONSTRAINT produse_pret_ck CHECK ( pret > 0 );
ALTER TABLE produse ADD CHECK ( um IN ( 'L', 'buc', 'g', 'kg', 'mL' ) );
ALTER TABLE produse AUTO_INCREMENT = 1000;

CREATE TABLE tipuri_produse (
    id_tip       TINYINT     NOT NULL AUTO_INCREMENT,
    denumire_tip VARCHAR(25) NOT NULL,
    CONSTRAINT tipuri_produse_pk PRIMARY KEY ( id_tip )
);
ALTER TABLE tipuri_produse
    ADD CONSTRAINT tipuri_produse_denumire_tip_ck CHECK ( 
	( char_length(denumire_tip) > 3 )AND ( REGEXP_LIKE ( denumire_tip,'^[A-Za-zăîâșțĂÎÂȘȚ ]+$' ) ) );
ALTER TABLE tipuri_produse ADD CONSTRAINT tipuri_produse_denumire_tip_un UNIQUE ( denumire_tip );

CREATE TABLE vanzari (
    nr_card         BIGINT   NOT NULL,
    id_produs       BIGINT   NOT NULL,
    nr_bon          BIGINT   NOT NULL AUTO_INCREMENT,
    cantitate       TINYINT  NOT NULL,
    data_achizitiei DATETIME,
    CONSTRAINT vanzari_pk PRIMARY KEY ( nr_bon )
);

ALTER TABLE detalii_clienti
    ADD CONSTRAINT detalii_clienti_clienti_fk FOREIGN KEY ( nr_card )
        REFERENCES clienti ( nr_card );

ALTER TABLE produse
    ADD CONSTRAINT produse_furnizori_fk FOREIGN KEY ( id_furnizor )
        REFERENCES furnizori ( id_furnizor );

ALTER TABLE produse
    ADD CONSTRAINT produse_tipuri_produse_fk FOREIGN KEY ( id_tip )
        REFERENCES tipuri_produse ( id_tip );

ALTER TABLE produse
    ADD CONSTRAINT produse_categorii_animaele_fk FOREIGN KEY ( id_categorie )
        REFERENCES categorii_animale ( id_categorie );

ALTER TABLE vanzari
    ADD CONSTRAINT vanzari_clienti_fk FOREIGN KEY ( nr_card )
        REFERENCES clienti ( nr_card );

ALTER TABLE vanzari
    ADD CONSTRAINT vanzari_produse_fk FOREIGN KEY ( id_produs )
        REFERENCES produse ( id_produs );

delimiter |
CREATE TRIGGER trg_vanzari_BRIU 
    BEFORE INSERT ON vanzari 
    FOR EACH ROW 
BEGIN
	IF NEW.data_achizitiei <= STR_TO_DATE('01.01.2000', '%d.%m.%Y')
	THEN
		SIGNAL SQLSTATE '50001'
		SET MESSAGE_TEXT = 'Dată invalidă! Data trebuie să fie mai mare decăt data deschiderii magazinului.';
END IF;
END;
|
delimiter ;


