# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 00:04:11 2018

@author: johnny
"""

import tensorflow as tf
import test
import numpy as np



def weight_variable(name, shape, init=None):
    if init is not None:
        initial = tf.get_variable(name, shape, 
                                  initializer = tf.constant_initializer(value = init))
    else:
        initial = tf.get_variable(name = name,shape=shape,
           initializer=tf.contrib.layers.xavier_initializer())
    return tf.Variable(initial)

def bias_variable(name, shape, init = None):
    if init is not None:
        initial = tf.get_variable(name, shape=shape, 
                              initializer=tf.constant_initializer(value = init))
    else:
        initial = initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    # stride [1, x_movement, y_movement, 1]
    # Must have strides[0] = strides[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    # stride [1, x_movement, y_movement, 1]
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

def batch_norm(x, n_out, phase_train):
    """
    Batch normalization on convolutional maps.
    Ref.: http://stackoverflow.com/questions/33949786/how-could-i-use-batch-normalization-in-tensorflow
    Args:
        x:           Tensor, 4D BHWD input maps
        n_out:       integer, depth of input maps
        phase_train: boolean tf.Varialbe, true indicates training phase
        scope:       string, variable scope
    Return:
        normed:      batch-normalized maps
    """
    with tf.variable_scope('bn'):
        beta = tf.Variable(tf.constant(0.0, shape=[n_out]),
                                     name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[n_out]),
                                      name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0,1,2], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.5)
        """
        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)
        mean, var = tf.cond(phase_train,
                            mean_var_with_update,
                            lambda: (ema.average(batch_mean), ema.average(batch_var)))
        """
        def mean_var_with_update():
                ema_apply_op = ema.apply([batch_mean, batch_var])
                with tf.control_dependencies([ema_apply_op]):
                    return tf.identity(batch_mean), tf.identity(batch_var)
        mean, var = mean_var_with_update()
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return normed


class net():
    def __init__(self):
        D = np.load("C:/Users/johnny/Downloads/vgg19.npy", encoding = 'latin1')
        #print(D.item().get('conv5_1'))
        self.W_conv1_1 = weight_variable("W_conv1_1", [3, 3, 3, 64], D.item().get('conv1_1')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv1_1 = bias_variable('b_conv1_1',[64], D.item().get('conv1_1')[1])
        self.W_conv1_2 = weight_variable("W_conv1_2", [3, 3, 64, 64], D.item().get('conv1_2')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv1_2 = bias_variable('b_conv1_2',[64], D.item().get('conv1_2')[1])
        
        self.W_conv2_1 = weight_variable("W_conv2_1", [3, 3, 64, 128], D.item().get('conv2_1')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv2_1 = bias_variable('b_conv2_1',[128], D.item().get('conv2_1')[1])
        self.W_conv2_2 = weight_variable("W_conv2_2", [3, 3, 128, 128], D.item().get('conv2_2')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv2_2 = bias_variable('b_conv2_2',[128], D.item().get('conv2_2')[1])
        
        self.W_conv3_1 = weight_variable("W_conv3_1", [3, 3, 128, 256], D.item().get('conv3_1')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv3_1 = bias_variable('b_conv3_1',[256], D.item().get('conv3_1')[1])
        self.W_conv3_2 = weight_variable("W_conv3_2", [3, 3, 256, 256], D.item().get('conv3_2')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv3_2 = bias_variable('b_conv3_2',[256], D.item().get('conv3_2')[1])
        self.W_conv3_3 = weight_variable("W_conv3_3", [3, 3, 256, 256], D.item().get('conv3_3')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv3_3 = bias_variable('b_conv3_3',[256], D.item().get('conv3_3')[1])
        self.W_conv3_4 = weight_variable("W_conv3_4", [3, 3, 256, 256], D.item().get('conv3_4')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv3_4 = bias_variable('b_conv3_4',[256], D.item().get('conv3_4')[1])
        
        self.W_conv4_1 = weight_variable("W_conv4_1", [3, 3, 256, 512], D.item().get('conv4_1')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv4_1 = bias_variable('b_conv4_1',[512], D.item().get('conv4_1')[1])
        self.W_conv4_2 = weight_variable("W_conv4_2", [3, 3, 512, 512], D.item().get('conv4_2')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv4_2 = bias_variable('b_conv4_2',[512], D.item().get('conv4_2')[1])
        
        self.W_conv4_3 = weight_variable("W_conv4_3", [3, 3, 512, 256]) # patch 5x5, in size 1, out size 32
        self.b_conv4_3 = bias_variable('b_conv4_3',[256])
        self.W_conv4_4 = weight_variable("W_conv4_4", [3, 3, 256, 256]) # patch 5x5, in size 1, out size 32
        self.b_conv4_4 = bias_variable('b_conv4_4',[256])
        """
        self.W_conv5_1 = weight_variable("W_conv5_1", [3, 3, 512, 512], D.item().get('conv5_1')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv5_1 = bias_variable('b_conv5_1',[512], D.item().get('conv5_1')[1])
        self.W_conv5_2 = weight_variable("W_conv5_2", [3, 3, 512, 512], D.item().get('conv5_2')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv5_2 = bias_variable('b_conv5_2',[512], D.item().get('conv5_2')[1])
        self.W_conv5_3 = weight_variable("W_conv5_3", [3, 3, 512, 512], D.item().get('conv5_3')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv5_3 = bias_variable('b_conv5_3',[512], D.item().get('conv5_3')[1])
        self.W_conv5_4 = weight_variable("W_conv5_4", [3, 3, 512, 512], D.item().get('conv5_4')[0]) # patch 5x5, in size 1, out size 32
        self.b_conv5_4 = bias_variable('b_conv5_4',[512], D.item().get('conv5_4')[1])
        """
        
    def vgg_pr_10(self, img, phase_train):
        h_conv1_1 = conv2d(img, self.W_conv1_1) + self.b_conv1_1 # output size 28x28x32
        h_conv1_1_bn = tf.nn.relu(batch_norm(h_conv1_1, 64, phase_train))
        h_conv1_2 = conv2d(h_conv1_1_bn, self.W_conv1_2) + self.b_conv1_2 # output size
        h_conv1_2_bn = tf.nn.relu(batch_norm(h_conv1_2, 64, phase_train))
        h_pool1 = max_pool_2x2(h_conv1_2_bn)
        
        h_conv2_1 = conv2d(h_pool1, self.W_conv2_1) + self.b_conv2_1 # output size 28x2
        h_conv2_1_bn = tf.nn.relu(batch_norm(h_conv2_1, 128, phase_train))
        h_conv2_2 = conv2d(h_conv2_1_bn, self.W_conv2_2) + self.b_conv2_2 # output size
        h_conv2_2_bn = tf.nn.relu(batch_norm(h_conv2_2, 128, phase_train))
        h_pool2 = max_pool_2x2(h_conv2_2_bn)
        
        h_conv3_1 = conv2d(h_pool2, self.W_conv3_1) + self.b_conv3_1 # output size 28x2
        h_conv3_1_bn = tf.nn.relu(batch_norm(h_conv3_1, 256, phase_train))
        h_conv3_2 = conv2d(h_conv3_1_bn, self.W_conv3_2) + self.b_conv3_2 # output size
        h_conv3_2_bn = tf.nn.relu(batch_norm(h_conv3_2, 256, phase_train))
        h_conv3_3 = conv2d(h_conv3_2_bn, self.W_conv3_3) + self.b_conv3_3 # output size
        h_conv3_3_bn = tf.nn.relu(batch_norm(h_conv3_3, 256, phase_train))
        h_conv3_4 = conv2d(h_conv3_3_bn, self.W_conv3_4) + self.b_conv3_4 # output size
        h_conv3_4_bn = tf.nn.relu(batch_norm(h_conv3_4, 256, phase_train))
        h_pool3 = max_pool_2x2(h_conv3_4_bn)
        
        h_conv4_1 = conv2d(h_pool3, self.W_conv4_1) + self.b_conv4_1 # output size 28x2
        h_conv4_1_bn = tf.nn.relu(batch_norm(h_conv4_1, 512, phase_train))
        h_conv4_2 = conv2d(h_conv4_1_bn, self.W_conv4_2) + self.b_conv4_2 # output size
        h_conv4_2_bn = tf.nn.relu(batch_norm(h_conv4_2, 512, phase_train))
        h_conv4_3 = conv2d(h_conv4_2_bn, self.W_conv4_3) + self.b_conv4_3 # output size
        h_conv4_3_bn = tf.nn.relu(batch_norm(h_conv4_3, 256, phase_train))
        h_conv4_4 = conv2d(h_conv4_3_bn, self.W_conv4_4) + self.b_conv4_4 # output size
        h_conv4_4_bn = tf.nn.relu(batch_norm(h_conv4_4, 256, phase_train))
        
        
        return h_conv4_4_bn

if __name__ == '__main__':
    imgs, labels, test_imgs, test_labels = test.return_all_data()
    batch_xs = [imgs[0], imgs[1], imgs[2]]
    with tf.Session() as sess:        
        x_im = tf.placeholder(tf.float32, [None, 32, 32, 3])
        net = net()
        net_out = net.vgg(x_im)
        init = tf.global_variables_initializer()
        sess.run(init)
        print(sess.run(net_out, feed_dict={x_im: batch_xs}))