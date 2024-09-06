from curation.domains.grist_mill_exchange import turkey_export, turkey_import

DOMAIN_SERVICE_MAP = {
    "gme_tr_im_bol": turkey_import,
    "gme_tr_ex_bol": turkey_export,
}
