;; Auto-generated. Do not edit!


(when (boundp 'tutorials::multiplier)
  (if (not (find-package "TUTORIALS"))
    (make-package "TUTORIALS"))
  (shadow 'multiplier (find-package "TUTORIALS")))
(unless (find-package "TUTORIALS::MULTIPLIER")
  (make-package "TUTORIALS::MULTIPLIER"))
(unless (find-package "TUTORIALS::MULTIPLIERREQUEST")
  (make-package "TUTORIALS::MULTIPLIERREQUEST"))
(unless (find-package "TUTORIALS::MULTIPLIERRESPONSE")
  (make-package "TUTORIALS::MULTIPLIERRESPONSE"))

(in-package "ROS")





(defclass tutorials::multiplierRequest
  :super ros::object
  :slots (_a _b ))

(defmethod tutorials::multiplierRequest
  (:init
   (&key
    ((:a __a) 0.0)
    ((:b __b) 0.0)
    )
   (send-super :init)
   (setq _a (float __a))
   (setq _b (float __b))
   self)
  (:a
   (&optional __a)
   (if __a (setq _a __a)) _a)
  (:b
   (&optional __b)
   (if __b (setq _b __b)) _b)
  (:serialization-length
   ()
   (+
    ;; float32 _a
    4
    ;; float32 _b
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _a
       (sys::poke _a (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _b
       (sys::poke _b (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _a
     (setq _a (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _b
     (setq _b (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(defclass tutorials::multiplierResponse
  :super ros::object
  :slots (_result ))

(defmethod tutorials::multiplierResponse
  (:init
   (&key
    ((:result __result) 0.0)
    )
   (send-super :init)
   (setq _result (float __result))
   self)
  (:result
   (&optional __result)
   (if __result (setq _result __result)) _result)
  (:serialization-length
   ()
   (+
    ;; float32 _result
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _result
       (sys::poke _result (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _result
     (setq _result (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(defclass tutorials::multiplier
  :super ros::object
  :slots ())

(setf (get tutorials::multiplier :md5sum-) "75900da305351b83210613bd5136a6e2")
(setf (get tutorials::multiplier :datatype-) "tutorials/multiplier")
(setf (get tutorials::multiplier :request) tutorials::multiplierRequest)
(setf (get tutorials::multiplier :response) tutorials::multiplierResponse)

(defmethod tutorials::multiplierRequest
  (:response () (instance tutorials::multiplierResponse :init)))

(setf (get tutorials::multiplierRequest :md5sum-) "75900da305351b83210613bd5136a6e2")
(setf (get tutorials::multiplierRequest :datatype-) "tutorials/multiplierRequest")
(setf (get tutorials::multiplierRequest :definition-)
      "float32 a
float32 b
---
float32 result
")

(setf (get tutorials::multiplierResponse :md5sum-) "75900da305351b83210613bd5136a6e2")
(setf (get tutorials::multiplierResponse :datatype-) "tutorials/multiplierResponse")
(setf (get tutorials::multiplierResponse :definition-)
      "float32 a
float32 b
---
float32 result
")



(provide :tutorials/multiplier "75900da305351b83210613bd5136a6e2")


