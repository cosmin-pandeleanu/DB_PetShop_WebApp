---  CATEGORII ANIMALE  ---
INSERT INTO categorii_animale(denumire_categorie) VALUES 
('câini'), ('pisici'), ('păsări'),
('rozătoare'), ('pești'), ('reptile');

---  TIPURI PRODUSE  ---
INSERT INTO tipuri_produse(denumire_tip) VALUES
('hrană') , ('suplimente nutritive'),
('produse de îngrijire'), ('accesorii'), ('jucării');

---  FURNIZORI  ---
INSERT INTO furnizori(denumire_furnizor) VALUES
('Whiskas'), ('Purina'), ('Felix'), ('Brit Premium'), ('Royal Canin'),
('Happy Dog'), ('Flamingo'), ('Petra Aqua'), ('Tetra');

---  CLIENTI  ---
INSERT INTO clienti(nume_client) VALUES 
('FĂRĂ CARD'), 
('Robert Popa'), 
('Ana Maria'),
('Bianca Popa'),
('Ionuț Marian'),
('Petru Ionică'),
('Răzvan Mitică');

--- DETALII CLIENTI ---
INSERT INTO detalii_clienti(email , data_nasterii, gen, adresa, oras) VALUES 
(null, null ,null, null, null),
('robert1605@yahoo.com',    STR_TO_DATE('16.05.2000', '%d.%m.%Y'), 'M',  null, 'Iași'),
('anaa-maria@gmail.com',    STR_TO_DATE('15.01.2001', '%d.%m.%Y'), 'F', 'str.Ștefan cel Mare, 23', 'Vaslui'),
('biia-popa@ymail.com',     STR_TO_DATE('10.09.1999', '%d.%m.%Y'), 'F', 'str.Mihai Viteazul, 25', 'Botoșani'),
('ionutz-marian@gmail.com', STR_TO_DATE('11.10.1989', '%d.%m.%Y'), 'M', 'str.Voiezorilor, 75', 'București'),
('petru.ionica89@gmail.com',STR_TO_DATE('21.11.1998', '%d.%m.%Y'), 'M', 'str.Apelor, 175', 'București'),
('razvan_mitica@gmail.com', STR_TO_DATE('25.11.2000', '%d.%m.%Y'), 'M', 'str.Florilor, 165', 'Iași');

--- PRODUSE ---
INSERT INTO produse(denumire_produs, stoc, pret, um, id_furnizor, id_categorie, id_tip) VALUES
('Hrană uscată', 100, 10.0, 'kg',  1, 2, 1),
('Minge roșie',  100, 5.0,  'buc', 5, 1, 5),
('Hrană umedă',  100, 10.0, 'buc', 3, 2, 1),
('Vitamine Mix', 100, 25.0, 'buc', 6, 3, 2),
('Semințe',      100, 5.5,  'kg',  3, 3, 1),
('Așternut',     100, 20.0, 'L',   3, 3, 3),
('Lesă',         100, 30.0, 'buc', 5, 1, 4),
('Acvariu',      100, 125.0,'buc', 4, 5, 4);

--- VANZARI ---
INSERT INTO vanzari(nr_card, id_produs, cantitate, data_achizitiei) VALUES (2, 1000, 2, SYSDATE());
UPDATE produse SET stoc = stoc-2 WHERE id_produs = 1000;
