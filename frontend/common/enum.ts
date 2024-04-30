enum LOADING {
    DEFAULT = 0,
    PHRASED = 1,
    PHRASE_DONE = 2,
    DONE = 3,
    RESULT = 4,
    LOADING = 5,
    ERROR = 9,
}

enum DatasetStatus {
    PENDING = 0,
    APPROVED = 1,
    REJECTED = 2,
}

export { LOADING, DatasetStatus }
