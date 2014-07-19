ALTER type enum_ticket_state ADD VALUE 'generating' after 'recorded';
ALTER type enum_ticket_state ADD VALUE 'generated' after 'generating';

INSERT into tbl_ticket_state VALUES ('recording', 'generating', 0, 10, true), ('recording', 'generated', 0, 5, false);
UPDATE tbl_ticket_state SET sort = sort + 2 WHERE ticket_type = 'recording' AND sort > 4;
UPDATE tbl_ticket_state SET sort = 5 WHERE ticket_type = 'recording' AND ticket_state = 'generating';
UPDATE tbl_ticket_state SET sort = 6 WHERE ticket_type = 'recording' AND ticket_state = 'generated';
