//! Implements Compression and Decompression for `Datasets` and `Clusters`.

use crate::core::dataset::Dataset;
use crate::core::number::Number;

pub trait CodecDataset<T: Number, U: Number>: Dataset<T, U> {
    /// Encodes the target instance in terms of the reference and produces the
    /// encoding as a vec of bytes.
    fn encode(&self, reference: &[T], target: &[T]) -> Vec<u8>;

    /// Decodes a target instance from a reference instance and an encoding.
    fn decode(&self, reference: &[T], encoding: &[u8]) -> Vec<T>;
}
