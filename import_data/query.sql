
SELECT posesje.miejscowosc, posesje.ulica, srodkowy_numer as numer,   sr_na_pos*il_pos as ilosc_koszy, il_pos as ilosc_posesji
from
  (SELECT miejscowosc, ulica, CEIL(sum(k110+1.4*k240+3*k1100)/count(*)) as sr_na_pos
    from wywozy
    inner join posesje
    on posesje.id=id_pos
    where co="kom"
    group by miejscowosc, ulica)
    as posesje
  INNER JOIN (SELECT miejscowosc, ulica, FLOOR(max(numer)/2) as srodkowy_numer,  count(*) as il_pos
    from posesje
    group by miejscowosc, ulica) as ilpos
    ON posesje.miejscowosc=ilpos.miejscowosc AND posesje.ulica=ilpos.ulica
order by miejscowosc, ulica