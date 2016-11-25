package utils;

import org.apache.hadoop.io.*;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

/**
 * Created by zhengyaolin on 2016/10/12.
 *
 * Description: tag the key to stand for the different data source
 *
 */
public class TextPair implements WritableComparable<TextPair>{
    private Text first = new Text();
    private Text second = new Text();

    public TextPair() {}

    public TextPair(Text first, Text second) {
        set(first, second);
    }

    public TextPair(String first, String second) {
        set(new Text(first), new Text(second));
    }

    public void set(Text first, Text second) {
        this.first = first;
        this.second = second;
    }

    /** Set the first of this TextPair. */
    public void setFirst(Text first) {
        this.first = first;
    }

    /** Return the first of this TextPair. */
    public Text getFirst() {
        return first;
    }

    /** Set the second of this TextPair. */
    public void setSecond(Text second) {
        this.second = second;
    }

    /** Return the second of this TextPair. */
    public Text getSecond() {
        return second;
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        first.readFields(in);
        second.readFields(in);
    }

    @Override
    public void write(DataOutput out) throws IOException {
        first.write(out);
        second.write(out);
    }

    /**
     * Compares two TextPair.
     * used for sorting in map and reduce, grouping in reduce
     *
     * */
    @Override
    public int compareTo(TextPair tp) {
        int cmp = first.compareTo(tp.first);
        if (cmp == 0) {
            return second.compareTo(tp.second);
        }
        return cmp;
    }

    /** Return true if other o equals to this o. */
    @Override
    public boolean equals(Object o) {
        if (o instanceof TextPair) {
            TextPair tp = (TextPair) o;
            return first.equals(tp.first) && second.equals(tp.second);
        }
        return false;
    }

    @Override
    public String toString() {
        return first.toString() + "," + second.toString();
    }

    /**
    @Override
    public int hashCode() {
        return first.hashCode() * 163 + second.hashCode();
    }
    */

    /** A Comparator optimized for TextPair.
    public static class Comparator extends WritableComparator {
        private static final Text.Comparator TEXT_COMPARATOR = new Text.Comparator();
        @Override
        public int compare(byte[] b1, int s1, int l1,
                           byte[] b2, int s2, int l2) {
            int firstL1 = WritableUtils.decodeVIntSize(b1[s1]) + readInt(b1, s1);
            int firstL2 = WritableUtils.decodeVIntSize(b2[s2]) + readInt(b2, s2);
            int secondL1 = WritableUtils.decodeVIntSize(b1[s1 + firstL1]) + readInt(b1, s1 + firstL1);
            int secondL2 = WritableUtils.decodeVIntSize(b1[s2 + firstL2]) + readInt(b2, s2 + firstL2);
            int cmp = TEXT_COMPARATOR.compare(b1, s1, firstL1, b2, s2, firstL2);
            if(cmp == 0)
                return TEXT_COMPARATOR.compare(b1, s1 + firstL1, secondL1, b2, s2 + firstL2, secondL2);
            return cmp;
        }

        @Override
        public int compare(WritableComparable a, WritableComparable b) {
            if(a instanceof TextPair && b instanceof TextPair) {
                return ((TextPair) a).second.compareTo(((TextPair) b).second);
            }
            return super.compare(a, b);
        }
    }
     */
}
