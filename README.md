# miee-otc-compression-labs

### file structure

info | bytes
--- | ---
`signature` | `2E 43 45 59 4D`  (`.CEYM` in ASCII)
`name_len` | 1 byte integer
`name` | depends on `name_length` (utf-8 text)
`freq_table_len` | 1 byte integer
`freq_table_chunks` | see `freq_table_lenght` (stucture below)
`data_chunks` | (stucture below)

#### frequency table chunk stucture 

info | bytes
--- | ---
`symbol` | 1 byte integer
`n_significant_bits` | 1 byte integer
`significant_bits` | see `n_significant_bits`

#### data chunk stucture

info | bytes
--- | ---
`chunk_bit_len` | 1 byte integer
`data` | see `chunk_bit_len`
