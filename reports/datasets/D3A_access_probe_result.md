# D3A Access Probe Result ? UCSF-PDGM

## Date
2026-05-12

## Dataset Candidate
D3A ? UCSF-PDGM

## Probe Method
A Python TCIA/NBIA metadata probe was performed using `tcia-utils`.

The probe attempted:

1. Listing available collections using `nbia.getCollections`.
2. Searching available collection names for UCSF, PDGM, GLIOMA, and BRAIN.
3. Querying possible UCSF-PDGM collection names using `nbia.getPatient`.
4. Querying possible UCSF-PDGM collection names using `nbia.getSeries`.

## Result

The local `tcia-utils` installation successfully returned a list of 154 available collections.

However, the collection search did not return UCSF-PDGM. The only glioma-related match returned by the collection search was:

- ICDC-Glioma

The following UCSF-PDGM candidate names returned no patient or series rows:

- UCSF-PDGM
- UCSF PDGM
- UCSF-PDGM-v3
- UCSF-PDGM-V3
- UCSF-PDGM-v4
- UCSF-PDGM-V4

## Interpretation

UCSF-PDGM remains a strong academic candidate, but it is not currently accessible through the tested `tcia-utils` NBIA query route.

This does not prove the dataset is unavailable. It means the current API route may not expose the collection under the expected name, or acquisition may require a TCIA manifest/Data Retriever route instead of direct NBIA query.

## Decision

Do not download UCSF-PDGM yet.

Investigate TCIA-accessible alternatives first, especially `ICDC-Glioma`, because it is visible through the current API collection list.

## Next Step

Probe `ICDC-Glioma` using `tcia-utils` to determine whether it is usable as D3 or D3B.
